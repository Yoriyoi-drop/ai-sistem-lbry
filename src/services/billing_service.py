"""
Stripe Billing Integration Service for Infinite AI Security Platform
Handles subscription management, payment processing, and billing events
Based on B2B SaaS transformation strategy
"""
from typing import Dict, Any, Optional, List
import stripe
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
import logging

from src.database.models import Organization, OrganizationSubscription, SubscriptionPlan, SubscriptionStatus
from src.config import settings

# Configure Stripe
stripe.api_key = settings.stripe_secret_key

logger = logging.getLogger(__name__)


class StripeBillingService:
    def __init__(self, db_session: Session):
        self.db = db_session
        
        if not settings.stripe_secret_key:
            logger.warning("Stripe secret key not configured. Billing functionality will be disabled.")

    def create_stripe_customer(self, organization: Organization) -> Optional[str]:
        """Create a Stripe customer for an organization"""
        if not settings.stripe_secret_key:
            return None
            
        try:
            customer = stripe.Customer.create(
                name=organization.name,
                email=organization.billing_email,
                metadata={
                    'organization_id': str(organization.id),
                    'organization_name': organization.name
                }
            )
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer for organization {organization.id}: {str(e)}")
            return None

    def create_subscription(self, organization_id: uuid.UUID, plan_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Create a subscription for an organization using Stripe"""
        if not settings.stripe_secret_key:
            return None
            
        # Get organization and plan details
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        plan = self.db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()
        
        if not organization or not plan:
            raise ValueError("Organization or plan not found")
        
        # Create Stripe customer if not exists
        if not organization.stripe_customer_id:
            stripe_customer_id = self.create_stripe_customer(organization)
            if not stripe_customer_id:
                return None
            
            organization.stripe_customer_id = stripe_customer_id
            self.db.commit()
        else:
            stripe_customer_id = organization.stripe_customer_id
        
        try:
            # Create subscription in Stripe
            # Note: You would need to create these products and prices in your Stripe dashboard first
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer_id,
                items=[
                    {
                        # This price_id should correspond to the plan in Stripe dashboard
                        # For now, we'll use the plan's tier as a reference
                        "price": self._get_stripe_price_id(plan.tier.value),
                    },
                ],
                metadata={
                    'organization_id': str(organization.id),
                    'plan_id': str(plan.id)
                },
                # Trial period for new customers
                trial_period_days=14 if plan.tier.value == "starter" else 0
            )
            
            # Create local subscription record
            local_subscription = OrganizationSubscription(
                organization_id=organization_id,
                plan_id=plan_id,
                status=SubscriptionStatus.ACTIVE.value,
                started_at=datetime.fromtimestamp(stripe_subscription.created),
                trial_ends_at=datetime.fromtimestamp(stripe_subscription.trial_end) if stripe_subscription.trial_end else None,
                auto_renew=True
            )
            
            self.db.add(local_subscription)
            self.db.commit()
            self.db.refresh(local_subscription)
            
            return {
                "id": str(local_subscription.id),
                "stripe_subscription_id": stripe_subscription.id,
                "status": local_subscription.status,
                "started_at": local_subscription.started_at.isoformat(),
                "trial_ends_at": local_subscription.trial_ends_at.isoformat() if local_subscription.trial_ends_at else None,
                "auto_renew": local_subscription.auto_renew
            }
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe subscription for organization {organization_id}: {str(e)}")
            return None

    def _get_stripe_price_id(self, tier: str) -> str:
        """
        Map our tier names to Stripe price IDs
        These should be created in your Stripe dashboard
        """
        price_mapping = {
            "starter": "price_starter_monthly",  # This needs to be created in Stripe dashboard
            "professional": "price_professional_monthly",
            "enterprise": "price_enterprise_monthly"
        }
        return price_mapping.get(tier, "price_starter_monthly")

    def update_subscription(self, organization_id: uuid.UUID, new_plan_id: uuid.UUID) -> bool:
        """Update an organization's subscription to a new plan"""
        if not settings.stripe_secret_key:
            return False
            
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        new_plan = self.db.query(SubscriptionPlan).filter(SubscriptionPlan.id == new_plan_id).first()
        
        if not organization or not new_plan:
            return False
        
        # Get the current subscription
        current_subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == organization_id
        ).first()
        
        if not current_subscription or not organization.stripe_customer_id:
            return False
        
        try:
            # Find the existing Stripe subscription
            stripe_subscriptions = stripe.Subscription.list(
                customer=organization.stripe_customer_id,
                status='active'
            )
            
            if not stripe_subscriptions or len(stripe_subscriptions.data) == 0:
                return False
            
            stripe_subscription = stripe_subscriptions.data[0]
            
            # Update the subscription with the new price
            updated_stripe_subscription = stripe.Subscription.modify(
                stripe_subscription.id,
                items=[{
                    'id': stripe_subscription.items.data[0].id,
                    'price': self._get_stripe_price_id(new_plan.tier.value),
                }],
                proration_behavior='always_invoice'  # Charge prorated amount immediately
            )
            
            # Update local subscription record
            current_subscription.plan_id = new_plan_id
            current_subscription.updated_at = datetime.utcnow()
            
            self.db.commit()
            return True
        except stripe.error.StripeError as e:
            logger.error(f"Failed to update Stripe subscription for organization {organization_id}: {str(e)}")
            return False

    def cancel_subscription(self, organization_id: uuid.UUID, at_period_end: bool = True) -> bool:
        """Cancel an organization's subscription"""
        if not settings.stripe_secret_key:
            return False
            
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        
        if not organization or not organization.stripe_customer_id:
            return False
        
        try:
            # Find the existing Stripe subscription
            stripe_subscriptions = stripe.Subscription.list(
                customer=organization.stripe_customer_id,
                status='active'
            )
            
            if not stripe_subscriptions or len(stripe_subscriptions.data) == 0:
                return False
            
            stripe_subscription = stripe_subscriptions.data[0]
            
            if at_period_end:
                # Cancel at the end of the current billing period
                canceled_subscription = stripe.Subscription.modify(
                    stripe_subscription.id,
                    cancel_at_period_end=True
                )
            else:
                # Cancel immediately
                canceled_subscription = stripe.Subscription.delete(
                    stripe_subscription.id
                )
            
            # Update local subscription record
            local_subscription = self.db.query(OrganizationSubscription).filter(
                OrganizationSubscription.organization_id == organization_id
            ).first()
            
            if local_subscription:
                local_subscription.status = SubscriptionStatus.CANCELLED.value
                local_subscription.auto_renew = False
                if not at_period_end:
                    local_subscription.status = SubscriptionStatus.EXPIRED.value
                    local_subscription.ends_at = datetime.utcnow()
                
                self.db.commit()
            
            return True
        except stripe.error.StripeError as e:
            logger.error(f"Failed to cancel Stripe subscription for organization {organization_id}: {str(e)}")
            return False

    def handle_stripe_webhook(self, payload: str, signature: str, webhook_secret: str) -> bool:
        """Handle incoming Stripe webhook events"""
        if not settings.stripe_secret_key:
            return False
            
        try:
            event = stripe.Webhook.construct_event(payload, signature, webhook_secret)
        except ValueError:
            # Invalid payload
            logger.error("Invalid payload in Stripe webhook")
            return False
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            logger.error("Invalid signature in Stripe webhook")
            return False
        
        event_type = event['type']
        event_data = event['data']['object']
        
        try:
            if event_type == 'customer.subscription.created':
                self._handle_subscription_created(event_data)
            elif event_type == 'customer.subscription.updated':
                self._handle_subscription_updated(event_data)
            elif event_type == 'customer.subscription.deleted':
                self._handle_subscription_deleted(event_data)
            elif event_type == 'invoice.payment_succeeded':
                self._handle_payment_succeeded(event_data)
            elif event_type == 'invoice.payment_failed':
                self._handle_payment_failed(event_data)
            
            return True
        except Exception as e:
            logger.error(f"Error handling Stripe webhook event {event_type}: {str(e)}")
            return False

    def _handle_subscription_created(self, event_data: Dict[str, Any]):
        """Handle subscription created webhook event"""
        # Extract organization ID from metadata
        metadata = event_data.get('metadata', {})
        organization_id_str = metadata.get('organization_id')
        plan_id_str = metadata.get('plan_id')
        
        if not organization_id_str or not plan_id_str:
            logger.warning("Organization ID or Plan ID not found in subscription metadata")
            return
        
        try:
            organization_id = uuid.UUID(organization_id_str)
            plan_id = uuid.UUID(plan_id_str)
        except ValueError:
            logger.warning("Invalid UUID in subscription metadata")
            return
        
        # Update local subscription status
        local_subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == organization_id
        ).first()
        
        if local_subscription:
            local_subscription.status = SubscriptionStatus.ACTIVE.value
            local_subscription.auto_renew = True
            local_subscription.started_at = datetime.fromtimestamp(event_data['created'])
            
            if event_data.get('trial_end'):
                local_subscription.trial_ends_at = datetime.fromtimestamp(event_data['trial_end'])
            
            if event_data.get('current_period_end'):
                local_subscription.ends_at = datetime.fromtimestamp(event_data['current_period_end'])
            
            self.db.commit()

    def _handle_subscription_updated(self, event_data: Dict[str, Any]):
        """Handle subscription updated webhook event"""
        # Extract organization ID from metadata
        metadata = event_data.get('metadata', {})
        organization_id_str = metadata.get('organization_id')
        
        if not organization_id_str:
            logger.warning("Organization ID not found in subscription metadata")
            return
        
        try:
            organization_id = uuid.UUID(organization_id_str)
        except ValueError:
            logger.warning("Invalid UUID in subscription metadata")
            return
        
        # Update local subscription
        local_subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == organization_id
        ).first()
        
        if local_subscription:
            if event_data.get('status') == 'active':
                local_subscription.status = SubscriptionStatus.ACTIVE.value
            elif event_data.get('status') == 'canceled':
                local_subscription.status = SubscriptionStatus.CANCELLED.value
            
            local_subscription.auto_renew = not event_data.get('cancel_at_period_end', False)
            
            if event_data.get('current_period_end'):
                local_subscription.ends_at = datetime.fromtimestamp(event_data['current_period_end'])
            
            self.db.commit()

    def _handle_subscription_deleted(self, event_data: Dict[str, Any]):
        """Handle subscription deleted/cancelled webhook event"""
        # Extract organization ID from metadata
        metadata = event_data.get('metadata', {})
        organization_id_str = metadata.get('organization_id')
        
        if not organization_id_str:
            logger.warning("Organization ID not found in subscription metadata")
            return
        
        try:
            organization_id = uuid.UUID(organization_id_str)
        except ValueError:
            logger.warning("Invalid UUID in subscription metadata")
            return
        
        # Update local subscription
        local_subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == organization_id
        ).first()
        
        if local_subscription:
            local_subscription.status = SubscriptionStatus.CANCELLED.value
            local_subscription.auto_renew = False
            local_subscription.ends_at = datetime.fromtimestamp(event_data.get('ended_at', event_data['current_period_end']))
            
            self.db.commit()

    def _handle_payment_succeeded(self, event_data: Dict[str, Any]):
        """Handle payment succeeded webhook event"""
        # Extract customer ID from invoice
        customer_id = event_data.get('customer')
        
        if not customer_id:
            logger.warning("Customer ID not found in payment event")
            return
        
        # Find organization by Stripe customer ID
        organization = self.db.query(Organization).filter(
            Organization.stripe_customer_id == customer_id
        ).first()
        
        if organization:
            # Update subscription status to active if it was past due
            local_subscription = self.db.query(OrganizationSubscription).filter(
                OrganizationSubscription.organization_id == organization.id
            ).first()
            
            if local_subscription and local_subscription.status == SubscriptionStatus.PAST_DUE.value:
                local_subscription.status = SubscriptionStatus.ACTIVE.value
                self.db.commit()

    def _handle_payment_failed(self, event_data: Dict[str, Any]):
        """Handle payment failed webhook event"""
        # Extract customer ID from invoice
        customer_id = event_data.get('customer')
        
        if not customer_id:
            logger.warning("Customer ID not found in payment event")
            return
        
        # Find organization by Stripe customer ID
        organization = self.db.query(Organization).filter(
            Organization.stripe_customer_id == customer_id
        ).first()
        
        if organization:
            # Update subscription status to past due
            local_subscription = self.db.query(OrganizationSubscription).filter(
                OrganizationSubscription.organization_id == organization.id
            ).first()
            
            if local_subscription:
                local_subscription.status = SubscriptionStatus.PAST_DUE.value
                self.db.commit()

    def get_billing_portal_url(self, organization_id: uuid.UUID, return_url: str) -> Optional[str]:
        """Generate a billing portal URL for an organization to manage their subscription"""
        if not settings.stripe_secret_key:
            return None
            
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        
        if not organization or not organization.stripe_customer_id:
            return None
        
        try:
            session = stripe.billing_portal.Session.create(
                customer=organization.stripe_customer_id,
                return_url=return_url
            )
            return session.url
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create billing portal session for organization {organization_id}: {str(e)}")
            return None

    def get_payment_method(self, organization_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get the payment method for an organization"""
        if not settings.stripe_secret_key:
            return None
            
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        
        if not organization or not organization.stripe_customer_id:
            return None
        
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=organization.stripe_customer_id,
                type='card'
            )
            
            if payment_methods.data:
                pm = payment_methods.data[0]  # Get the default payment method
                return {
                    'id': pm.id,
                    'type': pm.type,
                    'card_brand': pm.card.brand,
                    'card_last4': pm.card.last4,
                    'card_exp_month': pm.card.exp_month,
                    'card_exp_year': pm.card.exp_year,
                    'is_default': True  # Stripe treats the first one as default
                }
        
            return None
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve payment method for organization {organization_id}: {str(e)}")
            return None

    def get_invoices(self, organization_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Get invoices for an organization"""
        if not settings.stripe_secret_key:
            return []
            
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        
        if not organization or not organization.stripe_customer_id:
            return []
        
        try:
            invoices = stripe.Invoice.list(
                customer=organization.stripe_customer_id,
                limit=10  # Get last 10 invoices
            )
            
            return [
                {
                    'id': invoice.id,
                    'amount': invoice.amount_due / 100.0,  # Convert from cents to dollars
                    'status': invoice.status,
                    'created': datetime.fromtimestamp(invoice.created).isoformat(),
                    'due_date': datetime.fromtimestamp(invoice.due_date).isoformat() if invoice.due_date else None,
                    'hosted_invoice_url': invoice.hosted_invoice_url
                }
                for invoice in invoices
            ]
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve invoices for organization {organization_id}: {str(e)}")
            return []

    def get_usage_record_summary(self, organization_id: uuid.UUID) -> Dict[str, Any]:
        """Get usage-based billing summary for an organization"""
        if not settings.stripe_secret_key:
            return {}
        
        organization = self.db.query(Organization).filter(Organization.id == organization_id).first()
        
        if not organization or not organization.stripe_customer_id:
            return {}
        
        try:
            # Get subscription to identify usage-based items
            subscriptions = stripe.Subscription.list(
                customer=organization.stripe_customer_id,
                status='active'
            )
            
            if not subscriptions or len(subscriptions.data) == 0:
                return {}
            
            # Get current period usage
            subscription = subscriptions.data[0]
            usage_summary = {}
            
            for item in subscription.items.data:
                if item.price.recurring.usage_type == 'metered':
                    # Get usage records for this subscription item
                    usage_records = stripe.SubscriptionItem.list_usage_record_summaries(
                        item.id,
                        limit=10
                    )
                    
                    for record in usage_records:
                        usage_summary[record.id] = {
                            'subscription_item_id': item.id,
                            'total_usage': record.total_usage,
                            'period_start': datetime.fromtimestamp(record.period.start).isoformat(),
                            'period_end': datetime.fromtimestamp(record.period.end).isoformat()
                        }
            
            return {
                'organization_id': str(organization_id),
                'current_period_start': datetime.fromtimestamp(subscription.current_period_start).isoformat(),
                'current_period_end': datetime.fromtimestamp(subscription.current_period_end).isoformat(),
                'usage_summary': usage_summary
            }
        except stripe.error.StripeError as e:
            logger.error(f"Failed to retrieve usage records for organization {organization_id}: {str(e)}")
            return {}