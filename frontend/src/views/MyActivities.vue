<template>
  <div class="my-activities">
    <div class="page-header">
      <h1>我的活动</h1>
      <el-button type="primary" @click="$router.push('/create-activity')">
        <el-icon><Plus /></el-icon>
        创建活动
      </el-button>
    </div>

    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="我报名的活动" name="registered">
        <div v-if="registeredActivities.length > 0" class="activities-grid">
          <el-card 
            v-for="registration in registeredActivities" 
            :key="registration.id"
            class="activity-card"
            shadow="hover"
          >
            <div class="card-header">
              <h3 @click="goToDetail(registration.activity.id)">{{ registration.activity.title }}</h3>
              <el-tag :type="getRegistrationStatusType(registration.status)">
                {{ getRegistrationStatusText(registration.status) }}
              </el-tag>
            </div>
            
            <div class="card-content">
              <div class="info-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ formatDate(registration.activity.start_time) }}</span>
              </div>
              <div class="info-item">
                <el-icon><Location /></el-icon>
                <span>{{ registration.activity.location }}</span>
              </div>
              <div class="info-item">
                <el-icon><Clock /></el-icon>
                <span>{{ registration.activity.volunteer_hours }}小时</span>
              </div>
            </div>
            
            <div class="card-actions">
              <el-button 
                v-if="registration.status === 'registered' && canCheckIn(registration.activity)"
                type="success" 
                size="small"
                @click="checkIn(registration.id)"
              >
                签到
              </el-button>
              <el-button 
                v-if="registration.status === 'checked_in' && canComplete(registration.activity)"
                type="primary" 
                size="small"
                @click="showCompleteDialog(registration)"
              >
                完成活动
              </el-button>
              <el-button 
                v-if="registration.status === 'registered' && canCancel(registration.activity)"
                type="danger" 
                size="small"
                @click="cancelRegistration(registration.id)"
              >
                取消报名
              </el-button>
            </div>
          </el-card>
        </div>
        <el-empty v-else description="暂无报名的活动" />
      </el-tab-pane>

      <el-tab-pane label="我创建的活动" name="created">
        <div v-if="createdActivities.length > 0" class="activities-grid">
          <el-card 
            v-for="activity in createdActivities" 
            :key="activity.id"
            class="activity-card"
            shadow="hover"
          >
            <div class="card-header">
              <h3 @click="goToDetail(activity.id)">{{ activity.title }}</h3>
              <el-tag :type="getStatusType(activity.status)">
                {{ getStatusText(activity.status) }}
              </el-tag>
            </div>
            
            <div class="card-content">
              <div class="info-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ formatDate(activity.start_time) }}</span>
              </div>
              <div class="info-item">
                <el-icon><User /></el-icon>
                <span>{{ activity.current_participants }}/{{ activity.max_participants }}人</span>
              </div>
              <div class="info-item">
                <el-icon><Clock /></el-icon>
                <span>{{ activity.volunteer_hours }}小时</span>
              </div>
            </div>
            
            <div class="card-actions">
              <el-button size="small" @click="viewParticipants(activity.id)">
                查看参与者
              </el-button>
              <el-button 
                v-if="activity.status === 'active'"
                type="warning" 
                size="small"
                @click="editActivity(activity.id)"
              >
                编辑
              </el-button>
            </div>
          </el-card>
        </div>
        <el-empty v-else description="暂无创建的活动" />
      </el-tab-pane>
    </el-tabs>

    <!-- 完成活动对话框 -->
    <el-dialog v-model="completeDialogVisible" title="完成活动" width="400px">
      <el-form :model="completeForm" label-width="80px">
        <el-form-item label="评分">
          <el-rate v-model="completeForm.rating" :max="5" show-text />
        </el-form-item>
        <el-form-item label="反馈">
          <el-input 
            v-model="completeForm.feedback" 
            type="textarea" 
            :rows="4" 
            placeholder="请输入您的反馈意见"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="completeActivity" :loading="loading">
          确认完成
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Plus, Calendar, Location, User, Clock } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

export default {
  name: 'MyActivities',
  components: {
    Plus,
    Calendar,
    Location,
    User,
    Clock
  },
  data() {
    return {
      activeTab: 'registered',
      loading: false,
      completeDialogVisible: false,
      completeForm: {
        rating: 5,
        feedback: ''
      },
      currentRegistration: null
    }
  },
  computed: {
    ...mapState('activities', ['registeredActivities', 'createdActivities'])
  },
  async created() {
    await this.loadMyActivities()
  },
  methods: {
    ...mapActions('activities', [
      'fetchMyRegistrations',
      'fetchMyCreatedActivities',
      'checkInActivity',
      'completeActivityRegistration',
      'cancelActivityRegistration'
    ]),
    async loadMyActivities() {
      try {
        if (this.activeTab === 'registered') {
          await this.fetchMyRegistrations()
        } else {
          await this.fetchMyCreatedActivities()
        }
      } catch (error) {
        this.$message.error('加载活动列表失败')
      }
    },
    async handleTabChange(tab) {
      this.activeTab = tab
      await this.loadMyActivities()
    },
    goToDetail(activityId) {
      this.$router.push(`/activities/${activityId}`)
    },
    async checkIn(registrationId) {
      try {
        await this.checkInActivity(registrationId)
        this.$message.success('签到成功！')
        await this.loadMyActivities()
      } catch (error) {
        this.$message.error(error.message || '签到失败')
      }
    },
    showCompleteDialog(registration) {
      this.currentRegistration = registration
      this.completeForm.rating = 5
      this.completeForm.feedback = ''
      this.completeDialogVisible = true
    },
    async completeActivity() {
      this.loading = true
      try {
        await this.completeActivityRegistration({
          registrationId: this.currentRegistration.id,
          rating: this.completeForm.rating,
          feedback: this.completeForm.feedback
        })
        this.$message.success('活动完成！')
        this.completeDialogVisible = false
        await this.loadMyActivities()
      } catch (error) {
        this.$message.error(error.message || '完成活动失败')
      } finally {
        this.loading = false
      }
    },
    async cancelRegistration(registrationId) {
      try {
        await this.$confirm('确定要取消报名吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await this.cancelActivityRegistration(registrationId)
        this.$message.success('取消报名成功！')
        await this.loadMyActivities()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error(error.message || '取消报名失败')
        }
      }
    },
    viewParticipants(activityId) {
      // 这里可以跳转到参与者列表页面或显示参与者对话框
      this.$message.info('查看参与者功能待开发')
    },
    editActivity(activityId) {
      this.$router.push(`/edit-activity/${activityId}`)
    },
    canCheckIn(activity) {
      const now = dayjs()
      const startTime = dayjs(activity.start_time)
      const endTime = dayjs(activity.end_time)
      return now.isAfter(startTime.subtract(30, 'minute')) && now.isBefore(endTime)
    },
    canComplete(activity) {
      const now = dayjs()
      const endTime = dayjs(activity.end_time)
      return now.isAfter(endTime.subtract(30, 'minute'))
    },
    canCancel(activity) {
      const now = dayjs()
      const startTime = dayjs(activity.start_time)
      return startTime.isAfter(now.add(2, 'hour'))
    },
    formatDate(date) {
      return dayjs(date).format('MM-DD HH:mm')
    },
    getRegistrationStatusType(status) {
      const statusMap = {
        'registered': 'primary',
        'checked_in': 'success',
        'completed': 'success',
        'cancelled': 'info'
      }
      return statusMap[status] || 'info'
    },
    getRegistrationStatusText(status) {
      const statusMap = {
        'registered': '已报名',
        'checked_in': '已签到',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || '未知'
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
.my-activities {
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

.activities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.activity-card {
  transition: transform 0.2s;
}

.activity-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  margin: 0;
  color: #303133;
  cursor: pointer;
  transition: color 0.2s;
}

.card-header h3:hover {
  color: #409eff;
}

.card-content {
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.info-item .el-icon {
  color: #909399;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .my-activities {
    padding: 10px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .activities-grid {
    grid-template-columns: 1fr;
  }
  
  .card-actions {
    justify-content: center;
  }
}
</style>