<template>
  <div class="activity-detail">
    <el-card v-if="activity" class="activity-card">
      <div class="activity-header">
        <h1>{{ activity.title }}</h1>
        <el-tag :type="getStatusType(activity.status)">{{ getStatusText(activity.status) }}</el-tag>
      </div>
      
      <div class="activity-content">
        <div class="activity-info">
          <div class="info-item">
            <el-icon><Calendar /></el-icon>
            <span>开始时间：{{ formatDate(activity.start_time) }}</span>
          </div>
          <div class="info-item">
            <el-icon><Calendar /></el-icon>
            <span>结束时间：{{ formatDate(activity.end_time) }}</span>
          </div>
          <div class="info-item">
            <el-icon><Location /></el-icon>
            <span>活动地点：{{ activity.location }}</span>
          </div>
          <div class="info-item">
            <el-icon><User /></el-icon>
            <span>参与人数：{{ activity.current_participants }}/{{ activity.max_participants }}</span>
          </div>
          <div class="info-item">
            <el-icon><Clock /></el-icon>
            <span>志愿时长：{{ activity.volunteer_hours }}小时</span>
          </div>
          <div class="info-item">
            <el-icon><Phone /></el-icon>
            <span>联系方式：{{ activity.contact_info }}</span>
          </div>
        </div>
        
        <div class="activity-description">
          <h3>活动描述</h3>
          <p>{{ activity.description }}</p>
        </div>
        
        <div v-if="activity.requirements" class="activity-requirements">
          <h3>参与要求</h3>
          <p>{{ activity.requirements }}</p>
        </div>
      </div>
      
      <div class="activity-actions" v-if="isLoggedIn">
        <el-button 
          v-if="!isRegistered && activity.status === 'active' && !activity.is_full"
          type="primary" 
          @click="registerActivity"
          :loading="loading"
        >
          报名参加
        </el-button>
        <el-button 
          v-if="isRegistered && canUnregister"
          type="danger" 
          @click="unregisterActivity"
          :loading="loading"
        >
          取消报名
        </el-button>
        <el-tag v-if="activity.is_full" type="warning">活动已满员</el-tag>
        <el-tag v-if="activity.status !== 'active'" type="info">活动已结束</el-tag>
      </div>
    </el-card>
    
    <el-card v-else class="loading-card">
      <el-skeleton :rows="8" animated />
    </el-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Calendar, Location, User, Clock, Phone } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

export default {
  name: 'ActivityDetail',
  components: {
    Calendar,
    Location,
    User,
    Clock,
    Phone
  },
  data() {
    return {
      activity: null,
      loading: false,
      isRegistered: false
    }
  },
  computed: {
    ...mapState('auth', ['isLoggedIn']),
    canUnregister() {
      if (!this.activity) return false
      const now = dayjs()
      const startTime = dayjs(this.activity.start_time)
      return startTime.isAfter(now)
    }
  },
  async created() {
    await this.loadActivity()
    if (this.isLoggedIn) {
      await this.checkRegistrationStatus()
    }
  },
  methods: {
    ...mapActions('activities', ['fetchActivity', 'registerForActivity', 'unregisterFromActivity']),
    async loadActivity() {
      try {
        const id = this.$route.params.id
        this.activity = await this.fetchActivity(id)
      } catch (error) {
        this.$message.error('加载活动详情失败')
        this.$router.push('/activities')
      }
    },
    async checkRegistrationStatus() {
      // 这里应该调用API检查用户是否已报名
      // 暂时简化处理
    },
    async registerActivity() {
      if (!this.isLoggedIn) {
        this.$message.warning('请先登录')
        this.$router.push('/login')
        return
      }
      
      this.loading = true
      try {
        await this.registerForActivity(this.activity.id)
        this.$message.success('报名成功！')
        this.isRegistered = true
        await this.loadActivity() // 重新加载活动信息
      } catch (error) {
        this.$message.error(error.message || '报名失败')
      } finally {
        this.loading = false
      }
    },
    async unregisterActivity() {
      this.loading = true
      try {
        await this.unregisterFromActivity(this.activity.id)
        this.$message.success('取消报名成功！')
        this.isRegistered = false
        await this.loadActivity() // 重新加载活动信息
      } catch (error) {
        this.$message.error(error.message || '取消报名失败')
      } finally {
        this.loading = false
      }
    },
    formatDate(date) {
      return dayjs(date).format('YYYY-MM-DD HH:mm')
    },
    getStatusType(status) {
      const statusMap = {
        'active': 'success',
        'completed': 'info',
        'cancelled': 'danger'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'active': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || '未知'
    }
  }
}
</script>

<style scoped>
.activity-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.activity-card {
  margin-bottom: 20px;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.activity-header h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.activity-content {
  margin-bottom: 20px;
}

.activity-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}

.info-item .el-icon {
  color: #409eff;
}

.activity-description,
.activity-requirements {
  margin-bottom: 20px;
}

.activity-description h3,
.activity-requirements h3 {
  color: #303133;
  margin-bottom: 10px;
  font-size: 18px;
}

.activity-description p,
.activity-requirements p {
  color: #606266;
  line-height: 1.6;
  margin: 0;
}

.activity-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.loading-card {
  min-height: 400px;
}

@media (max-width: 768px) {
  .activity-detail {
    padding: 10px;
  }
  
  .activity-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .activity-info {
    grid-template-columns: 1fr;
  }
  
  .activity-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>