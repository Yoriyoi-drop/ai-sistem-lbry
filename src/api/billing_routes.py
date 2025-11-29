"""
Billing API Routes for Stripe Integration
Based on B2B SaaS transformation strategy
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import uuid

from src.database.session import get_db
from src.services.billing_service import StripeBillingService
from src.middleware.multitenant import get_current_organization_id
from src.config import settings


router = APIRouter(prefix="/billing", tags=["Billing & Subscriptions"])


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Stripe webhook endpoint to handle subscription events
    """
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    if not settings.stripe_webhook_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe webhook secret not configured"
        )
    
    billing_service = StripeBillingService(db)
    
    try:
        result = billing_service.handle_stripe_webhook(
            payload.decode('utf-8'), 
            sig_header, 
            settings.stripe_webhook_secret
        )
        
        if result:
            return {"status": "success"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Webhook processing failed"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook error: {str(e)}"
        )


@router.post("/subscribe/{plan_id}")
async def create_subscription(
    plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Create a subscription for an organization
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    try:
        result = billing_service.create_subscription(current_org_id, plan_id)
        
        if result:
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create subscription"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating subscription: {str(e)}"
        )


@router.patch("/subscription/{new_plan_id}")
async def update_subscription(
    new_plan_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Update an organization's subscription to a new plan
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    success = billing_service.update_subscription(current_org_id, new_plan_id)
    
    if success:
        return {"status": "subscription updated", "organization_id": str(current_org_id)}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update subscription"
        )


@router.post("/unsubscribe")
async def cancel_subscription(
    at_period_end: bool = True,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Cancel an organization's subscription
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    success = billing_service.cancel_subscription(current_org_id, at_period_end)
    
    if success:
        return {"status": "subscription cancelled", "organization_id": str(current_org_id)}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to cancel subscription"
        )


@router.get("/billing-portal")
async def get_billing_portal(
    return_url: str,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get a billing portal URL for an organization to manage their subscription
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    portal_url = billing_service.get_billing_portal_url(current_org_id, return_url)
    
    if portal_url:
        return {"billing_portal_url": portal_url}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to generate billing portal URL"
        )


@router.get("/payment-method")
async def get_payment_method(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get the payment method for an organization
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    payment_method = billing_service.get_payment_method(current_org_id)
    
    if payment_method:
        return payment_method
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payment method found"
        )


@router.get("/invoices")
async def get_invoices(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get invoices for an organization
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    invoices = billing_service.get_invoices(current_org_id)
    return {"invoices": invoices, "organization_id": str(current_org_id)}


@router.get("/usage-summary")
async def get_usage_summary(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get usage-based billing summary for an organization
    """
    billing_service = StripeBillingService(db)
    
    if not settings.stripe_secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Stripe is not configured"
        )
    
    usage_summary = billing_service.get_usage_record_summary(current_org_id)
    return usage_summary