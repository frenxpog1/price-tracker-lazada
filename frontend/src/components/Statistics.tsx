/**
 * Statistics Dashboard Component
 * Shows key metrics about tracked products and savings
 */

import { useEffect, useState } from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: string;
  color: string;
  trend?: string;
}

function StatCard({ title, value, icon, color, trend }: StatCardProps) {
  return (
    <div className="bg-gradient-to-br from-dark-100/50 to-dark-50/30 backdrop-blur-sm border border-dark-200/50 rounded-2xl p-6 hover:scale-105 transition-all duration-300 hover:shadow-2xl hover:shadow-accent-blue/20 animate-slide-up">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-dark-500 text-sm font-medium mb-2">{title}</p>
          <p className={`text-3xl font-bold ${color} mb-1`}>{value}</p>
          {trend && (
            <p className="text-xs text-accent-green flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              {trend}
            </p>
          )}
        </div>
        <div className={`text-4xl ${color} opacity-80`}>{icon}</div>
      </div>
    </div>
  );
}

export default function Statistics() {
  const [stats, setStats] = useState({
    totalProducts: 0,
    activeAlerts: 0,
    moneySaved: 0,
    avgDiscount: 0,
  });

  useEffect(() => {
    // Simulate fetching statistics
    // In production, this would fetch from your API
    const mockStats = {
      totalProducts: 12,
      activeAlerts: 5,
      moneySaved: 3450,
      avgDiscount: 18,
    };
    
    // Animate numbers counting up
    const duration = 1000;
    const steps = 60;
    const interval = duration / steps;
    
    let step = 0;
    const timer = setInterval(() => {
      step++;
      const progress = step / steps;
      
      setStats({
        totalProducts: Math.floor(mockStats.totalProducts * progress),
        activeAlerts: Math.floor(mockStats.activeAlerts * progress),
        moneySaved: Math.floor(mockStats.moneySaved * progress),
        avgDiscount: Math.floor(mockStats.avgDiscount * progress),
      });
      
      if (step >= steps) {
        clearInterval(timer);
        setStats(mockStats);
      }
    }, interval);
    
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatCard
        title="Products Tracked"
        value={stats.totalProducts}
        icon="📦"
        color="text-accent-blue"
        trend="+3 this week"
      />
      <StatCard
        title="Active Alerts"
        value={stats.activeAlerts}
        icon="🔔"
        color="text-accent-purple"
        trend="+2 triggered"
      />
      <StatCard
        title="Money Saved"
        value={`₱${stats.moneySaved.toLocaleString()}`}
        icon="💰"
        color="text-accent-green"
        trend="+₱450 this month"
      />
      <StatCard
        title="Avg. Discount"
        value={`${stats.avgDiscount}%`}
        icon="📊"
        color="text-accent-orange"
        trend="+5% vs last month"
      />
    </div>
  );
}
