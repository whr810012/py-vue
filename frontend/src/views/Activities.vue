<template>
  <div class="activities-page">
    <div class="page-container">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-content">
          <h1>志愿活动</h1>
          <p>发现并参与有意义的志愿服务活动</p>
        </div>
        <el-button 
          type="primary" 
          size="large"
          @click="$router.push('/create-activity')"
          v-if="isLoggedIn"
        >
          <el-icon><Plus /></el-icon>
          发布活动
        </el-button>
      </div>

      <!-- 搜索和筛选 -->
      <div class="search-section">
        <el-card class="search-card">
          <div class="search-form">
            <div class="search-input">
              <el-input
                v-model="searchForm.search"
                placeholder="搜索活动标题或描述"
                size="large"
                clearable
                @keyup.enter="handleSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>
            
            <div class="filter-controls">
              <el-select
                v-model="searchForm.category"
                placeholder="选择分类"
                size="large"
                clearable
                @change="handleSearch"
              >
                <el-option label="环保公益" value="环保" />
                <el-option label="助老服务" value="助老" />
                <el-option label="教育支持" value="教育" />
                <el-option label="社区建设" value="社区" />
                <el-option label="文化活动" value="文化" />
                <el-option label="其他服务" value="其他" />
              </el-select>
              
              <el-select
                v-model="searchForm.status"
                placeholder="活动状态"
                size="large"
                @change="handleSearch"
              >
                <el-option label="进行中" value="active" />
                <el-option label="已完成" value="completed" />
                <el-option label="已取消" value="cancelled" />
              </el-select>
              
              <el-button 
                type="primary" 
                size="large"
                @click="handleSearch"
              >
                搜索
              </el-button>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 活动列表 -->
      <div class="activities-section">
        <div class="activities-grid" v-loading="loading">
          <div 
            v-for="activity in activities" 
            :key="activity.id" 
            class="activity-card"
            @click="$router.push(`/activities/${activity.id}`)"
          >
            <div class="activity-image">
              <img v-if="activity.image_url" :src="activity.image_url" :alt="activity.title" />
              <div v-else class="default-image">
                <el-icon><Calendar /></el-icon>
              </div>
              <div class="activity-status">
                <el-tag 
                  :type="getActivityStatusType(activity.status)"
                  size="small"
                >
                  {{ getActivityStatusText(activity.status) }}
                </el-tag>
              </div>
            </div>
            
            <div class="activity-content">
              <div class="activity-category" v-if="activity.category">
                <el-tag size="small" effect="plain">{{ activity.category }}</el-tag>
              </div>
              
              <h3 class="activity-title">{{ activity.title }}</h3>
              
              <div class="activity-meta">
                <div class="meta-item">
                  <el-icon><Location /></el-icon>
                  <span>{{ activity.location }}</span>
                </div>
                <div class="meta-item">
                  <el-icon><Clock /></el-icon>
                  <span>{{ formatDate(activity.start_time) }}</span>
                </div>
                <div class="meta-item" v-if="activity.volunteer_hours > 0">
                  <el-icon><Trophy /></el-icon>
                  <span>{{ activity.volunteer_hours }} 小时</span>
                </div>
              </div>
              
              <p class="activity-description">{{ activity.description }}</p>
              
              <div class="activity-footer">
                <div class="participant-info">
                  <el-icon><User /></el-icon>
                  <span>{{ activity.current_participants }}/{{ activity.max_participants }}</span>
                </div>
                
                <div class="activity-actions">
                  <el-button 
                    v-if="activity.is_active && !activity.is_full"
                    type="primary" 
                    size="small"
                    @click.stop="handleRegister(activity)"
                  >
                    立即报名
                  </el-button>
                  <el-button 
                    v-else-if="activity.is_full"
                    size="small"
                    disabled
                  >
                    已满员
                  </el-button>
                  <el-button 
                    v-else
                    size="small"
                    disabled
                  >
                    已结束
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-if="!loading && activities.length === 0" class="empty-state">
          <el-empty description="暂无活动数据">
            <el-button type="primary" @click="$router.push('/create-activity')" v-if="isLoggedIn">
              发布第一个活动
            </el-button>
          </el-empty>
        </div>
        
        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="pagination.total > 0">
          <el-pagination
            v-model:current-page="pagination.currentPage"
            :page-size="10"
            :total="pagination.total"
            layout="total, prev, pager, next, jumper"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import dayjs from 'dayjs'

export default {
  name: 'Activities',
  data() {
    return {
      searchForm: {
        search: '',
        category: '',
        status: 'active'
      }
    }
  },
  computed: {
    ...mapState('auth', ['isLoggedIn']),
    ...mapState('activities', ['activities', 'loading', 'pagination'])
  },
  methods: {
    ...mapActions('activities', ['fetchActivities', 'registerActivity']),
    
    async loadActivities() {
      const params = {
        page: this.pagination.currentPage,
        per_page: 10,
        ...this.searchForm
      }
      
      // 移除空值
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === null || params[key] === undefined) {
          delete params[key]
        }
      })
      
      try {
        await this.fetchActivities(params)
      } catch (error) {
        this.$message.error('加载活动失败')
      }
    },
    
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadActivities()
    },
    
    handlePageChange(page) {
      this.pagination.currentPage = page
      this.loadActivities()
    },
    
    async handleRegister(activity) {
      if (!this.isLoggedIn) {
        this.$message.warning('请先登录')
        this.$router.push('/login')
        return
      }
      
      try {
        await this.registerActivity({ activityId: activity.id, notes: '' })
        this.$message.success('报名成功')
        // 重新加载活动列表
        this.loadActivities()
      } catch (error) {
        if (error.response) {
          this.$message.error(error.response.data.error || '报名失败')
        } else {
          this.$message.error('报名失败，请重试')
        }
      }
    },
    
    formatDate(dateString) {
      return dayjs(dateString).format('MM-DD HH:mm')
    },
    
    getActivityStatusType(status) {
      const statusMap = {
        'active': 'success',
        'completed': 'info',
        'cancelled': 'danger'
      }
      return statusMap[status] || 'info'
    },
    
    getActivityStatusText(status) {
      const statusMap = {
        'active': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }
  },
  
  created() {
    // 从路由参数获取初始搜索条件
    if (this.$route.query.category) {
      this.searchForm.category = this.$route.query.category
    }
    
    this.loadActivities()
  }
}
</script>

<style lang="scss" scoped>
.activities-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
  
  .header-content {
    h1 {
      font-size: 32px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 8px;
    }
    
    p {
      color: #909399;
      font-size: 16px;
    }
  }
}

.search-section {
  margin-bottom: 30px;
  
  .search-card {
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }
  
  .search-form {
    display: flex;
    gap: 20px;
    align-items: flex-end;
    
    .search-input {
      flex: 1;
      min-width: 300px;
    }
    
    .filter-controls {
      display: flex;
      gap: 12px;
      
      .el-select {
        width: 140px;
      }
    }
  }
}

.activities-section {
  .activities-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
  }
  
  .activity-card {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .activity-image {
      position: relative;
      width: 100%;
      height: 200px;
      overflow: hidden;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      
      .default-image {
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-size: 48px;
      }
      
      .activity-status {
        position: absolute;
        top: 12px;
        right: 12px;
      }
    }
    
    .activity-content {
      padding: 20px;
      
      .activity-category {
        margin-bottom: 12px;
      }
      
      .activity-title {
        font-size: 18px;
        font-weight: 600;
        color: #303133;
        margin-bottom: 12px;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .activity-meta {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-bottom: 12px;
        
        .meta-item {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 14px;
          color: #606266;
          
          .el-icon {
            font-size: 16px;
          }
        }
      }
      
      .activity-description {
        color: #909399;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 16px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .activity-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        
        .participant-info {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 14px;
          color: #606266;
        }
      }
    }
  }
}

.empty-state {
  padding: 60px 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .search-form {
    flex-direction: column;
    align-items: stretch;
    
    .filter-controls {
      flex-wrap: wrap;
      
      .el-select {
        flex: 1;
        min-width: 120px;
      }
    }
  }
  
  .activities-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-meta {
    .meta-item {
      font-size: 13px;
    }
  }
}
</style>