import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { CreditCard, CheckCircle, BarChart3, Users, HardDrive } from 'lucide-react';
import { getSubscription, updateSubscription, getUsage } from '../services/api';

const Billing = () => {
  const [currentPlan, setCurrentPlan] = useState('free');
  const [usage, setUsage] = useState({});
  const [loading, setLoading] = useState(true);

  const plans = [
    {
      id: 'free',
      name: 'Free',
      price: '$0',
      period: 'per month',
      features: [
        'Up to 1 user',
        '1,000 API calls/month',
        '1GB storage',
        'Community support'
      ],
      buttonText: 'Current Plan',
      buttonVariant: 'outline',
      isCurrent: true
    },
    {
      id: 'standard',
      name: 'Standard',
      price: '$9.99',
      period: 'per month',
      features: [
        'Up to 5 users',
        '10,000 API calls/month',
        '10GB storage',
        'Email support',
        'Custom domains'
      ],
      buttonText: 'Upgrade',
      buttonVariant: 'default'
    },
    {
      id: 'professional',
      name: 'Professional',
      price: '$29.99',
      period: 'per month',
      features: [
        'Up to 20 users',
        '100,000 API calls/month',
        '100GB storage',
        'Priority email support',
        'Custom domains',
        'Advanced analytics'
      ],
      buttonText: 'Upgrade',
      buttonVariant: 'default'
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      price: '$99.99',
      period: 'per month',
      features: [
        'Up to 100 users',
        '1,000,000 API calls/month',
        '1000GB storage',
        '24/7 phone support',
        'Custom domains',
        'Advanced analytics',
        'Dedicated account manager'
      ],
      buttonText: 'Contact Sales',
      buttonVariant: 'default'
    }
  ];

  useEffect(() => {
    const fetchBillingInfo = async () => {
      try {
        const [subscriptionRes, usageRes] = await Promise.all([
          getSubscription(),
          getUsage()
        ]);
        
        setCurrentPlan(subscriptionRes.data.subscription.tier);
        setUsage(usageRes.data.usage);
      } catch (error) {
        console.error('Failed to fetch billing info:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBillingInfo();
  }, []);

  const handlePlanChange = async (planId) => {
    if (planId === currentPlan) return;
    
    try {
      await updateSubscription(planId);
      setCurrentPlan(planId);
      
      // In a real app, you would update the UI to reflect the new plan
      alert(`Successfully upgraded to ${planId} plan!`);
    } catch (error) {
      console.error('Failed to update subscription:', error);
      alert('Failed to update subscription. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="p-6 flex justify-center items-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">Billing & Subscription</h1>
          <p className="text-gray-600 mt-2">
            Manage your subscription and view usage statistics
          </p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Current Plan</p>
          <p className="text-xl font-semibold capitalize">{currentPlan}</p>
        </div>
      </div>

      {/* Usage Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <BarChart3 className="mr-2 h-5 w-5" />
            Usage Summary
          </CardTitle>
          <CardDescription>Your current usage against plan limits</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="border rounded-lg p-4">
              <div className="flex items-center mb-2">
                <HardDrive className="h-4 w-4 mr-2 text-blue-500" />
                <span className="text-sm font-medium">Storage</span>
              </div>
              <div className="text-2xl font-bold">
                {usage.storage_used_gb || '0'}GB
              </div>
              <div className="text-xs text-gray-500">
                of {(usage.storage_limit_gb || 10)}GB
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${(usage.storage_used_gb || 0) / (usage.storage_limit_gb || 10) * 100}%` }}
                ></div>
              </div>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center mb-2">
                <Users className="h-4 w-4 mr-2 text-green-500" />
                <span className="text-sm font-medium">API Calls</span>
              </div>
              <div className="text-2xl font-bold">
                {usage.api_calls_month || '0'}
              </div>
              <div className="text-xs text-gray-500">
                of {(usage.api_calls_limit_month || 1000)} monthly
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${(usage.api_calls_month || 0) / (usage.api_calls_limit_month || 1000) * 100}%` }}
                ></div>
              </div>
            </div>
            
            <div className="border rounded-lg p-4">
              <div className="flex items-center mb-2">
                <CreditCard className="h-4 w-4 mr-2 text-purple-500" />
                <span className="text-sm font-medium">Active Users</span>
              </div>
              <div className="text-2xl font-bold">
                {(usage.active_users || 1)}
              </div>
              <div className="text-xs text-gray-500">
                of {(usage.user_limit || 1)} users
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full" 
                  style={{ width: `${(usage.active_users || 1) / (usage.user_limit || 1) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Plan Selection */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Choose Your Plan</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {plans.map((plan) => (
            <Card 
              key={plan.id} 
              className={currentPlan === plan.id ? "border-2 border-blue-500 ring-1 ring-blue-500" : ""}
            >
              <CardHeader>
                <CardTitle>{plan.name}</CardTitle>
                <div className="flex items-baseline">
                  <span className="text-3xl font-bold">{plan.price}</span>
                  <span className="text-gray-500 ml-1">{plan.period}</span>
                </div>
                <CardDescription>{plan.name} plan features</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 mb-6">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2 mt-0.5" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button
                  className="w-full"
                  variant={plan.buttonVariant}
                  onClick={() => handlePlanChange(plan.id)}
                  disabled={plan.id === currentPlan}
                >
                  {plan.buttonText}
                </Button>
                {plan.id === currentPlan && (
                  <div className="text-center mt-2 text-sm text-green-600">
                    Current Plan
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Billing Information */}
      <Card>
        <CardHeader>
          <CardTitle>Billing Information</CardTitle>
          <CardDescription>Manage your payment methods and invoices</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-4 border rounded-lg">
              <div>
                <div className="font-medium">Payment Method</div>
                <div className="text-sm text-gray-500">Visa ending in 4242</div>
              </div>
              <Button variant="outline" size="sm">Update</Button>
            </div>
            
            <div className="flex justify-between items-center p-4 border rounded-lg">
              <div>
                <div className="font-medium">Next Billing Date</div>
                <div className="text-sm text-gray-500">June 1, 2024</div>
              </div>
            </div>
            
            <div className="flex justify-between items-center p-4 border rounded-lg">
              <div>
                <div className="font-medium">Invoices</div>
                <div className="text-sm text-gray-500">View and download past invoices</div>
              </div>
              <Button variant="outline" size="sm">View</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Billing;