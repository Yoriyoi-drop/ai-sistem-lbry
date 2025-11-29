"""
Usage Tracking Service for Consumption-Based Billing
Based on B2B SaaS transformation strategy
Tracks scans, API calls, agent hours, and other usage metrics
"""
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
import uuid

from src.database.models import Organization, UsageMetric, SecurityScan, AgentSession
from src.services.tier_service import TierService


class UsageTrackingService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.tier_service = TierService(db_session)

    def track_usage(self, organization_id: uuid.UUID, metric_type: str, 
                   quantity: int = 1, user_id: Optional[uuid.UUID] = None) -> bool:
        """
        Track usage for an organization
        """
        try:
            # Get the current period (first day of current month)
            current_date = datetime.utcnow().date()
            current_period = current_date.replace(day=1)
            
            # Check if we already have a usage record for this period
            usage_record = self.db.query(UsageMetric).filter(
                and_(
                    UsageMetric.organization_id == organization_id,
                    UsageMetric.metric_type == metric_type,
                    UsageMetric.period == current_period
                )
            ).first()
            
            if usage_record:
                # Update existing record
                usage_record.quantity += quantity
                usage_record.created_at = datetime.utcnow()
            else:
                # Create new record
                usage_record = UsageMetric(
                    organization_id=organization_id,
                    metric_type=metric_type,
                    quantity=quantity,
                    period=current_period
                )
                self.db.add(usage_record)
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error tracking usage: {e}")
            return False

    def get_usage_for_period(self, organization_id: uuid.UUID, metric_type: str, 
                           period: date) -> int:
        """Get usage for a specific metric type and period"""
        usage_record = self.db.query(UsageMetric).filter(
            and_(
                UsageMetric.organization_id == organization_id,
                UsageMetric.metric_type == metric_type,
                UsageMetric.period == period
            )
        ).first()
        
        return usage_record.quantity if usage_record else 0

    def get_current_usage(self, organization_id: uuid.UUID, metric_type: str) -> int:
        """Get current month usage for a specific metric type"""
        current_date = datetime.utcnow().date()
        current_period = current_date.replace(day=1)
        
        return self.get_usage_for_period(organization_id, metric_type, current_period)

    def get_usage_breakdown(self, organization_id: uuid.UUID, 
                          start_date: date, end_date: date) -> Dict[str, List[Dict]]:
        """Get detailed usage breakdown for a date range"""
        # Get all usage records for the organization in the date range
        usage_records = self.db.query(UsageMetric).filter(
            and_(
                UsageMetric.organization_id == organization_id,
                UsageMetric.period >= start_date.replace(day=1),  # Start from first day of month
                UsageMetric.period <= end_date.replace(day=1)     # End at first day of month
            )
        ).all()
        
        # Organize by metric type
        usage_breakdown = {}
        for record in usage_records:
            metric_type = record.metric_type
            if metric_type not in usage_breakdown:
                usage_breakdown[metric_type] = []
            
            usage_breakdown[metric_type].append({
                "period": record.period.isoformat(),
                "quantity": record.quantity,
                "date_recorded": record.created_at.isoformat()
            })
        
        return usage_breakdown

    def check_usage_limits(self, organization_id: uuid.UUID) -> Dict[str, Dict[str, int]]:
        """
        Check usage against limits for all metric types
        Returns a dictionary of metric types with current usage and limits
        """
        # Get organization's subscription limits
        limits = self.tier_service.get_organization_subscription_info(organization_id)["plan_details"]["limits"]
        
        # Common metric types for security platform
        metric_types = [
            "scans", 
            "api_calls", 
            "agent_hours", 
            "ai_credits",
            "data_storage_gb"
        ]
        
        usage_status = {}
        for metric_type in metric_types:
            # Handle different naming conventions in limits
            limit_key = f"max_{metric_type.replace('-', '_')}_per_month"
            if limit_key not in limits:
                # Try alternative naming
                alt_key = f"max_{metric_type.replace('-', '_')}"
                if alt_key in limits:
                    limit_key = alt_key
                else:
                    continue  # Skip if not in limits
            
            limit = limits[limit_key]
            current_usage = self.get_current_usage(organization_id, metric_type)
            
            usage_status[metric_type] = {
                "current_usage": current_usage,
                "limit": limit,
                "percentage_used": (current_usage / limit * 100) if limit > 0 else 0,
                "remaining": max(0, limit - current_usage) if limit > 0 else float('inf'),
                "over_limit": current_usage > limit if limit > 0 else False
            }
        
        return usage_status

    def get_usage_summary(self, organization_id: uuid.UUID, 
                         period: Optional[date] = None) -> Dict[str, any]:
        """Get a summary of usage for an organization"""
        if period is None:
            period = datetime.utcnow().date().replace(day=1)
        
        # Get all usage records for the period
        usage_records = self.db.query(UsageMetric).filter(
            and_(
                UsageMetric.organization_id == organization_id,
                UsageMetric.period == period
            )
        ).all()
        
        # Calculate summary
        total_usage = sum(record.quantity for record in usage_records)
        
        # Group by metric type
        usage_by_type = {}
        for record in usage_records:
            usage_by_type[record.metric_type] = record.quantity
        
        # Get limit information
        usage_limits = self.check_usage_limits(organization_id)
        
        return {
            "organization_id": str(organization_id),
            "period": period.isoformat(),
            "total_usage": total_usage,
            "usage_by_type": usage_by_type,
            "usage_limits": usage_limits,
            "date_generated": datetime.utcnow().isoformat()
        }

    def increment_scan_usage(self, organization_id: uuid.UUID, 
                           scan_cost_credits: float = 0.0) -> bool:
        """Increment scan usage for an organization"""
        # Track the scan
        scan_success = self.track_usage(organization_id, "scans", 1)
        
        # Track any cost credits if applicable
        if scan_cost_credits > 0:
            credits_int = int(scan_cost_credits * 1000)  # Convert to smaller unit to store as int
            self.track_usage(organization_id, "ai_credits", credits_int)
        
        return scan_success

    def increment_api_call_usage(self, organization_id: uuid.UUID, 
                               call_weight: int = 1) -> bool:
        """Increment API call usage for an organization"""
        return self.track_usage(organization_id, "api_calls", call_weight)

    def increment_agent_usage(self, organization_id: uuid.UUID, 
                            duration_seconds: int, agent_type: str = "general") -> bool:
        """Increment agent usage based on duration (convert seconds to hours)"""
        # Convert seconds to hours (rounded up to nearest hour for billing)
        hours = (duration_seconds + 3599) // 3600  # Round up to nearest hour
        
        # Track the agent hours
        success = self.track_usage(organization_id, "agent_hours", hours)
        
        # Also track specific agent type usage
        if agent_type:
            self.track_usage(organization_id, f"agent_{agent_type}_hours", hours)
        
        return success

    def get_billing_projection(self, organization_id: uuid.UUID) -> Dict[str, any]:
        """Get billing projection based on current usage patterns"""
        # Get current usage
        usage_summary = self.get_usage_summary(organization_id)
        
        # Get subscription info
        subscription_info = self.tier_service.get_organization_subscription_info(organization_id)
        plan_details = subscription_info["plan_details"]
        
        # Calculate projected usage for the month based on current usage
        current_date = datetime.utcnow().date()
        days_in_month = 30  # Approximation
        days_elapsed = current_date.day
        
        projection = {}
        for metric_type, usage_data in usage_summary["usage_by_type"].items():
            if metric_type in plan_details["limits"]:
                current_usage = usage_data
                projected_usage = int((current_usage / days_elapsed) * days_in_month)
                
                # Check if there's an overage cost structure
                overage_rate = self._get_overage_rate(metric_type)
                
                projection[metric_type] = {
                    "current_usage": current_usage,
                    "projected_usage": projected_usage,
                    "limit": plan_details["limits"][metric_type.replace('-', '_').replace(' ', '_')],
                    "overage_rate": overage_rate,
                    "estimated_overage": max(0, projected_usage - plan_details["limits"][metric_type.replace('-', '_').replace(' ', '_')]) * overage_rate if overage_rate else 0
                }
        
        # Calculate projected billing
        base_price = plan_details["price_monthly"]
        estimated_overage = sum(item["estimated_overage"] for item in projection.values())
        projected_total = base_price + estimated_overage
        
        return {
            "subscription_base_price": base_price,
            "estimated_overage": estimated_overage,
            "projected_total": projected_total,
            "usage_projection": projection,
            "projection_period": f"{current_date.year}-{current_date.month:02d}",
            "date_calculated": datetime.utcnow().isoformat()
        }

    def _get_overage_rate(self, metric_type: str) -> float:
        """Get the overage rate for a metric type"""
        # Define overage rates as per B2B strategy
        overage_rates = {
            "scans": 0.10,  # $0.10 per additional scan
            "api_calls": 0.001,  # $0.001 per additional API call
            "agent_hours": 4.00,  # $4.00 per agent hour
            "ai_credits": 0.001  # $0.001 per credit (if credits are a separate metric)
        }
        
        return overage_rates.get(metric_type, 0.0)

    def check_usage_allowance(self, organization_id: uuid.UUID, 
                            metric_type: str, requested_amount: int = 1) -> Tuple[bool, Dict[str, int]]:
        """
        Check if an organization can perform an action based on usage limits
        Returns (is_allowed, usage_info)
        """
        current_usage = self.get_current_usage(organization_id, metric_type)
        
        # Get limits for the organization's tier
        subscription_info = self.tier_service.get_organization_subscription_info(organization_id)
        plan_details = subscription_info["plan_details"]
        limits = plan_details["limits"]
        
        limit_key = f"max_{metric_type.replace('-', '_')}_per_month"
        if limit_key not in limits:
            # Try alternative format
            alt_key = f"max_{metric_type.replace('-', '_')}"
            if alt_key in limits:
                limit_key = alt_key
            else:
                # If no limit exists, assume unlimited
                return True, {
                    "current_usage": current_usage,
                    "limit": float('inf'),
                    "remaining": float('inf'),
                    "requested": requested_amount
                }
        
        limit = limits[limit_key]
        remaining = max(0, limit - current_usage)
        
        is_allowed = (remaining >= requested_amount) or (limit == 0)  # 0 means unlimited
        
        return is_allowed, {
            "current_usage": current_usage,
            "limit": limit,
            "remaining": remaining,
            "requested": requested_amount
        }