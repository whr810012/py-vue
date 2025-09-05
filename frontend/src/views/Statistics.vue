<template>
  <div class="statistics">
    <div class="page-header">
      <h1>统计数据</h1>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="loadStatistics"
        class="date-picker"
      />
    </div>

    <!-- 概览卡片 -->
    <div class="stats-overview">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon total">
            <el-icon><DataAnalysis /></el-icon>
          </div>
          <div class="stat-info">
            <h3>{{ stats.total_registrations || 0 }}</h3>
            <p>总报名次数</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon completed">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <h3>{{ stats.completed_activities || 0 }}</h3>
            <p>完成活动</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon hours">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <h3>{{ stats.total_volunteer_hours || 0 }}</h3>
            <p>志愿时长(小时)</p>
          </div>
        </div>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-icon created">
            <el-icon><Plus /></el-icon>
          </div>
          <div class="stat-info">
            <h3>{{ stats.created_activities || 0 }}</h3>
            <p>创建活动</p>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <span>活动参与趋势</span>
            </template>
            <div ref="participationChart" class="chart-container"></div>
          </el-card>
        </el-col>
        
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <span>活动状态分布</span>
            </template>
            <div ref="statusChart" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card class="chart-card">
            <template #header>
              <span>志愿时长统计</span>
            </template>
            <div ref="hoursChart" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 详细数据表格 -->
    <el-card class="table-card">
      <template #header>
        <span>活动记录</span>
      </template>
      
      <el-table :data="activityRecords" stripe>
        <el-table-column prop="activity_title" label="活动名称" />
        <el-table-column prop="registration_time" label="报名时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.registration_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="volunteer_hours" label="志愿时长" width="100">
          <template #default="{ row }">
            {{ row.volunteer_hours }}小时
          </template>
        </el-table-column>
        <el-table-column prop="rating" label="评分" width="100">
          <template #default="{ row }">
            <el-rate v-if="row.rating" :model-value="row.rating" disabled show-score />
            <span v-else>-</span>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="totalRecords"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadActivityRecords"
          @current-change="loadActivityRecords"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { DataAnalysis, CircleCheck, Clock, Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

export default {
  name: 'Statistics',
  components: {
    DataAnalysis,
    CircleCheck,
    Clock,
    Plus
  },
  data() {
    return {
      dateRange: [dayjs().subtract(30, 'day').toDate(), new Date()],
      stats: {},
      activityRecords: [],
      currentPage: 1,
      pageSize: 10,
      totalRecords: 0,
      charts: {
        participation: null,
        status: null,
        hours: null
      }
    }
  },
  async mounted() {
    await this.loadStatistics()
    await this.loadActivityRecords()
    this.initCharts()
  },
  beforeUnmount() {
    // 销毁图表实例
    Object.values(this.charts).forEach(chart => {
      if (chart) {
        chart.dispose()
      }
    })
  },
  methods: {
    ...mapActions('activities', ['fetchUserStatistics', 'fetchUserActivityRecords']),
    async loadStatistics() {
      try {
        const params = {}
        if (this.dateRange && this.dateRange.length === 2) {
          params.start_date = dayjs(this.dateRange[0]).format('YYYY-MM-DD')
          params.end_date = dayjs(this.dateRange[1]).format('YYYY-MM-DD')
        }
        this.stats = await this.fetchUserStatistics(params)
        this.updateCharts()
      } catch (error) {
        this.$message.error('加载统计数据失败')
      }
    },
    async loadActivityRecords() {
      try {
        const params = {
          page: this.currentPage,
          per_page: this.pageSize
        }
        if (this.dateRange && this.dateRange.length === 2) {
          params.start_date = dayjs(this.dateRange[0]).format('YYYY-MM-DD')
          params.end_date = dayjs(this.dateRange[1]).format('YYYY-MM-DD')
        }
        const result = await this.fetchUserActivityRecords(params)
        this.activityRecords = result.records || []
        this.totalRecords = result.total || 0
      } catch (error) {
        this.$message.error('加载活动记录失败')
      }
    },
    initCharts() {
      // 这里应该使用真实的图表库如 ECharts
      // 由于没有安装图表库，这里只是占位
      this.createMockChart('participationChart', '参与趋势图')
      this.createMockChart('statusChart', '状态分布图')
      this.createMockChart('hoursChart', '时长统计图')
    },
    createMockChart(refName, title) {
      const container = this.$refs[refName]
      if (container) {
        container.innerHTML = `
          <div style="
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f5f7fa;
            border-radius: 4px;
            color: #909399;
          ">
            ${title}（需要集成图表库）
          </div>
        `
      }
    },
    updateCharts() {
      // 更新图表数据
      // 这里应该根据 this.stats 更新图表
    },
    formatDate(date) {
      return dayjs(date).format('YYYY-MM-DD HH:mm')
    },
    getStatusType(status) {
      const statusMap = {
        'registered': 'primary',
        'checked_in': 'success',
        'completed': 'success',
        'cancelled': 'info'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'registered': '已报名',
        'checked_in': '已签到',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || '未知'
    }
  }
}
</script>

<style scoped>
.statistics {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.date-picker {
  width: 300px;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.completed {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon.hours {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon.created {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-info h3 {
  margin: 0 0 5px 0;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-info p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.charts-section {
  margin-bottom: 20px;
}

.chart-card {
  height: 400px;
}

.chart-container {
  height: 300px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .statistics {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .date-picker {
    width: 100%;
  }
  
  .stats-overview {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .stat-content {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
}
</style>