/**
 * Statistics Dashboard Component - 2026 Modern Design
 */

import { useEffect, useState } from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
}

function StatCard({ title, value, subtitle }: StatCardProps) {
  return (
    <div className="modern-card p-6">
      <p className="text-white/50 text-sm mb-2">{title}</p>
      <p className="text-3xl font-semibold text-white mb-1">{value}</p>
      {subtitle && (
        <p className="text-white/40 text-xs">{subtitle}</p>
      )}
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
    const mockStats = {
      totalProducts: 12,
      activeAlerts: 5,
      moneySaved: 3450,
      avgDiscount: 18,
    };
    
    // Simple count up
    const duration = 800;
    const steps = 40;
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
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8 fade-in">
      <StatCard
        title="Products Tracked"
        value={stats.totalProducts}
        subtitle="+3 this week"
      />
      <StatCard
        title="Active Alerts"
        value={stats.activeAlerts}
        subtitle="2 triggered today"
      />
      <StatCard
        title="Money Saved"
        value={`₱${stats.moneySaved.toLocaleString()}`}
        subtitle="+₱450 this month"
      />
      <StatCard
        title="Avg. Discount"
        value={`${stats.avgDiscount}%`}
        subtitle="vs last month"
      />
    </div>
  );
}
