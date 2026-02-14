<template>
  <div class="dashboard-stats" v-if="loading || stats">
    <!-- Loading State -->
    <div v-if="loading" class="dashboard-loading">
      <div class="spinner"></div>
      <p>正在加载仪表盘数据...</p>
    </div>

    <template v-else>
      <!-- Summary Cards -->
      <div class="stats-grid">
        <div class="stat-card total">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          </div>
          <div class="stat-info">
            <span class="stat-label">总投诉量</span>
            <span class="stat-value">{{ stats.total }}</span>
          </div>
        </div>
        
        <div class="stat-card pending">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          </div>
          <div class="stat-info">
            <span class="stat-label">待处理</span>
            <span class="stat-value">{{ stats.status_counts.pending || 0 }}</span>
          </div>
        </div>

        <div class="stat-card in-progress">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
          </div>
          <div class="stat-info">
            <span class="stat-label">处理中</span>
            <span class="stat-value">{{ stats.status_counts.in_progress || 0 }}</span>
          </div>
        </div>

        <div class="stat-card resolved">
          <div class="stat-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          </div>
          <div class="stat-info">
            <span class="stat-label">已解决</span>
            <span class="stat-value">{{ stats.status_counts.resolved || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-row">
        <!-- Status Distribution Pie Chart -->
        <div class="chart-card">
          <h3>问题状态分布</h3>
          <div class="chart-container">
            <Pie :data="pieData" :options="pieOptions" />
          </div>
        </div>

        <!-- Project Stats Bar Chart -->
        <div class="chart-card wide">
          <h3>各项目问题统计 (Top 5)</h3>
          <div class="chart-container">
            <Bar :data="barData" :options="barOptions" />
          </div>
        </div>
      </div>

      <!-- Project Status Table -->
      <div class="table-card" style="margin-bottom: 24px;">
        <h3>各项目问题状态统计</h3>
        <div class="simple-table-container">
            <table class="simple-table">
                <thead>
                    <tr>
                        <th>项目名称</th>
                        <th>待处理</th>
                        <th>处理中</th>
                        <th>已解决</th>
                        <th>总计</th>
                        <th class="text-right">解决进度</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(p, index) in stats.project_status_stats" :key="index">
                        <td class="font-bold">{{ p.name }}</td>
                        <td>
                            <span class="status-badge pending" v-if="p.pending > 0">{{ p.pending }}</span>
                            <span v-else class="text-muted">-</span>
                        </td>
                        <td>
                            <span class="status-badge in-progress" v-if="p.in_progress > 0">{{ p.in_progress }}</span>
                            <span v-else class="text-muted">-</span>
                        </td>
                        <td>
                            <span class="status-badge resolved" v-if="p.resolved > 0">{{ p.resolved }}</span>
                            <span v-else class="text-muted">-</span>
                        </td>
                        <td class="font-bold">{{ p.total }}</td>
                        <td class="text-right" style="width: 25%;">
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill resolved" :style="{ width: ((p.resolved / p.total) * 100) + '%' }"></div>
                            </div>
                            <span class="text-xs text-muted">{{ ((p.resolved / p.total) * 100).toFixed(0) }}%</span>
                        </td>
                    </tr>
                    <tr v-if="!stats.project_status_stats || stats.project_status_stats.length === 0">
                        <td colspan="6" class="text-center text-muted">暂无数据</td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>

      <!-- Type Breakdown Table -->
      <div class="table-card">
        <h3>问题类型统计</h3>
        <div class="simple-table-container">
            <table class="simple-table">
                <thead>
                    <tr>
                        <th>项目名称</th>
                        <th>类型名称</th>
                        <th>数量</th>
                        <th>占比</th>
                        <th class="text-right">进度条</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(type, index) in stats.type_counts" :key="index">
                        <td class="font-bold">{{ type.project_name }}</td>
                        <td>
                            <span class="type-badge">{{ type.name }}</span>
                        </td>
                        <td class="font-bold">{{ type.count }}</td>
                        <td>{{ ((type.count / stats.total) * 100).toFixed(1) }}%</td>
                        <td class="text-right" style="width: 40%;">
                            <div class="progress-bar-bg">
                                <div class="progress-bar-fill" :style="{ width: ((type.count / stats.total) * 100) + '%' }"></div>
                            </div>
                        </td>
                    </tr>
                    <tr v-if="stats.type_counts.length === 0">
                        <td colspan="5" class="text-center text-muted">暂无数据</td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Title } from 'chart.js'
import { Pie, Bar } from 'vue-chartjs'
import api from '../api'

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale, Title)

export default {
  name: 'DashboardStats',
  components: { Pie, Bar },
  data() {
    return {
      loading: true,
      stats: null
    }
  },
  computed: {
    pieData() {
      if (!this.stats) return null
      return {
        labels: ['待处理', '处理中', '已解决'],
        datasets: [
          {
            backgroundColor: ['#fbbf24', '#3b82f6', '#10b981'],
            data: [
              this.stats.status_counts.pending || 0,
              this.stats.status_counts.in_progress || 0,
              this.stats.status_counts.resolved || 0
            ]
          }
        ]
      }
    },
    pieOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right'
            }
        }
      }
    },
    barData() {
        if (!this.stats) return null
        return {
            labels: this.stats.project_counts.map(p => p.name),
            datasets: [
                {
                    label: '投诉数量',
                    backgroundColor: '#6366f1',
                    borderRadius: 6,
                    data: this.stats.project_counts.map(p => p.count)
                }
            ]
        }
    },
    barOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    }
  },
  async created() {
    await this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        const response = await api.get('complaints/dashboard_stats/')
        this.stats = response.data
      } catch (error) {
        console.error('Failed to fetch dashboard stats', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.dashboard-stats {
  margin-bottom: 32px;
}

.dashboard-loading {
  text-align: center;
  padding: 40px;
  color: #64748b;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  border: 1px solid #e2e8f0;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-card.total .stat-icon { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.stat-card.pending .stat-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
.stat-card.in-progress .stat-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.stat-card.resolved .stat-icon { background: linear-gradient(135deg, #10b981, #059669); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

/* Charts Row */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.chart-card h3, .table-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px 0;
}

.chart-container {
  height: 250px;
  position: relative;
}

/* Table Card */
.table-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.simple-table {
  width: 100%;
  border-collapse: collapse;
}

.simple-table th {
  text-align: left;
  padding: 12px;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: #64748b;
  border-bottom: 1px solid #f1f5f9;
}

.simple-table td {
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.95rem;
  color: #334155;
  vertical-align: middle;
}

.simple-table tr:last-child td {
  border-bottom: none;
}

.type-badge {
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #475569;
}

.progress-bar-bg {
  width: 100%;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: #6366f1;
  border-radius: 4px;
}

.progress-bar-fill.resolved {
    background: #10b981;
}

.status-badge {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}

.status-badge.pending { background: #fef3c7; color: #d97706; }
.status-badge.in-progress { background: #dbeafe; color: #2563eb; }
.status-badge.resolved { background: #d1fae5; color: #059669; }

.text-right { text-align: right; }
.text-xs { font-size: 0.75rem; }
.font-bold { font-weight: 600; color: #1e293b; }
.text-center { text-align: center; }
.text-muted { color: #94a3b8; }

/* Responsive */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>