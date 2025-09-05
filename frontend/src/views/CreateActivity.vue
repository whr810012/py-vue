<template>
  <div class="create-activity">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑活动' : '创建活动' }}</span>
          <el-button @click="$router.go(-1)">返回</el-button>
        </div>
      </template>

      <el-form 
        :model="activityForm" 
        :rules="rules" 
        ref="activityFormRef" 
        label-width="120px"
        class="activity-form"
      >
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="活动标题" prop="title">
              <el-input 
                v-model="activityForm.title" 
                placeholder="请输入活动标题"
                maxlength="100"
                show-word-limit
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="活动分类" prop="category">
              <el-select v-model="activityForm.category" placeholder="请选择活动分类">
                <el-option label="环保公益" value="environmental" />
                <el-option label="教育支持" value="education" />
                <el-option label="社区服务" value="community" />
                <el-option label="扶贫助困" value="poverty_relief" />
                <el-option label="文化传承" value="culture" />
                <el-option label="医疗健康" value="healthcare" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="志愿时长" prop="volunteer_hours">
              <el-input-number 
                v-model="activityForm.volunteer_hours" 
                :min="0.5" 
                :max="24" 
                :step="0.5"
                placeholder="小时"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="活动地点" prop="location">
              <el-input 
                v-model="activityForm.location" 
                placeholder="请输入活动地点"
                maxlength="200"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_time">
              <el-date-picker
                v-model="activityForm.start_time"
                type="datetime"
                placeholder="选择开始时间"
                style="width: 100%;"
                :disabled-date="disabledStartDate"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="end_time">
              <el-date-picker
                v-model="activityForm.end_time"
                type="datetime"
                placeholder="选择结束时间"
                style="width: 100%;"
                :disabled-date="disabledEndDate"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="参与人数" prop="max_participants">
              <el-input-number 
                v-model="activityForm.max_participants" 
                :min="1" 
                :max="1000"
                placeholder="人"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系方式" prop="contact_info">
              <el-input 
                v-model="activityForm.contact_info" 
                placeholder="请输入联系方式"
                maxlength="50"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="活动描述" prop="description">
          <el-input 
            v-model="activityForm.description" 
            type="textarea" 
            :rows="4" 
            placeholder="请详细描述活动内容、目的和意义"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="参与要求">
          <el-input 
            v-model="activityForm.requirements" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入参与活动的要求和注意事项（可选）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="活动图片">
          <el-upload
            class="image-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
            :http-request="uploadImage"
          >
            <img v-if="activityForm.image_url" :src="activityForm.image_url" class="uploaded-image" />
            <div v-else class="upload-placeholder">
              <el-icon class="upload-icon"><Plus /></el-icon>
              <div class="upload-text">点击上传活动图片</div>
            </div>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <div class="form-actions">
            <el-button @click="resetForm">重置</el-button>
            <el-button type="primary" @click="submitForm" :loading="loading">
              {{ isEdit ? '更新活动' : '创建活动' }}
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

export default {
  name: 'CreateActivity',
  components: {
    Plus
  },
  data() {
    return {
      loading: false,
      isEdit: false,
      activityId: null,
      activityForm: {
        title: '',
        description: '',
        location: '',
        start_time: null,
        end_time: null,
        max_participants: 10,
        category: '',
        volunteer_hours: 2,
        requirements: '',
        contact_info: '',
        image_url: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入活动标题', trigger: 'blur' },
          { min: 5, max: 100, message: '标题长度在 5 到 100 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入活动描述', trigger: 'blur' },
          { min: 20, max: 1000, message: '描述长度在 20 到 1000 个字符', trigger: 'blur' }
        ],
        location: [
          { required: true, message: '请输入活动地点', trigger: 'blur' }
        ],
        start_time: [
          { required: true, message: '请选择开始时间', trigger: 'change' }
        ],
        end_time: [
          { required: true, message: '请选择结束时间', trigger: 'change' },
          { validator: this.validateEndTime, trigger: 'change' }
        ],
        max_participants: [
          { required: true, message: '请输入参与人数', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择活动分类', trigger: 'change' }
        ],
        volunteer_hours: [
          { required: true, message: '请输入志愿时长', trigger: 'blur' }
        ],
        contact_info: [
          { required: true, message: '请输入联系方式', trigger: 'blur' }
        ]
      }
    }
  },
  async created() {
    // 检查是否为编辑模式
    if (this.$route.params.id) {
      this.isEdit = true
      this.activityId = this.$route.params.id
      await this.loadActivity()
    }
  },
  methods: {
    ...mapActions('activities', ['createActivity', 'updateActivity', 'fetchActivity']),
    async loadActivity() {
      try {
        const activity = await this.fetchActivity(this.activityId)
        this.activityForm = {
          title: activity.title,
          description: activity.description,
          location: activity.location,
          start_time: new Date(activity.start_time),
          end_time: new Date(activity.end_time),
          max_participants: activity.max_participants,
          category: activity.category,
          volunteer_hours: activity.volunteer_hours,
          requirements: activity.requirements || '',
          contact_info: activity.contact_info,
          image_url: activity.image_url || ''
        }
      } catch (error) {
        this.$message.error('加载活动信息失败')
        this.$router.push('/my-activities')
      }
    },
    async submitForm() {
      try {
        await this.$refs.activityFormRef.validate()
        this.loading = true
        
        const formData = {
          ...this.activityForm,
          start_time: dayjs(this.activityForm.start_time).format('YYYY-MM-DD HH:mm:ss'),
          end_time: dayjs(this.activityForm.end_time).format('YYYY-MM-DD HH:mm:ss')
        }
        
        if (this.isEdit) {
          await this.updateActivity({ id: this.activityId, ...formData })
          this.$message.success('活动更新成功！')
        } else {
          await this.createActivity(formData)
          this.$message.success('活动创建成功！')
        }
        
        this.$router.push('/my-activities')
      } catch (error) {
        if (error.message) {
          this.$message.error(error.message)
        }
      } finally {
        this.loading = false
      }
    },
    resetForm() {
      this.$refs.activityFormRef.resetFields()
      if (!this.isEdit) {
        this.activityForm = {
          title: '',
          description: '',
          location: '',
          start_time: null,
          end_time: null,
          max_participants: 10,
          category: '',
          volunteer_hours: 2,
          requirements: '',
          contact_info: '',
          image_url: ''
        }
      }
    },
    validateEndTime(rule, value, callback) {
      if (value && this.activityForm.start_time) {
        if (dayjs(value).isBefore(dayjs(this.activityForm.start_time))) {
          callback(new Error('结束时间不能早于开始时间'))
        } else if (dayjs(value).isSame(dayjs(this.activityForm.start_time))) {
          callback(new Error('结束时间不能等于开始时间'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    },
    disabledStartDate(time) {
      return time.getTime() < Date.now() - 24 * 60 * 60 * 1000
    },
    disabledEndDate(time) {
      if (this.activityForm.start_time) {
        return time.getTime() <= dayjs(this.activityForm.start_time).valueOf()
      }
      return time.getTime() < Date.now() - 24 * 60 * 60 * 1000
    },
    beforeImageUpload(file) {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt5M = file.size / 1024 / 1024 < 5

      if (!isJPG) {
        this.$message.error('图片只能是 JPG/PNG 格式!')
      }
      if (!isLt5M) {
        this.$message.error('图片大小不能超过 5MB!')
      }
      return isJPG && isLt5M
    },
    uploadImage(options) {
      // 这里应该上传到服务器，暂时使用本地预览
      const reader = new FileReader()
      reader.onload = (e) => {
        this.activityForm.image_url = e.target.result
      }
      reader.readAsDataURL(options.file)
    }
  }
}
</script>

<style scoped>
.create-activity {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.activity-form {
  margin-top: 20px;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.image-uploader {
  display: flex;
  justify-content: center;
}

.image-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: 0.2s;
  width: 300px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-uploader :deep(.el-upload:hover) {
  border-color: #409eff;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #8c939d;
}

.upload-icon {
  font-size: 28px;
  margin-bottom: 10px;
}

.upload-text {
  font-size: 14px;
}

.uploaded-image {
  width: 300px;
  height: 200px;
  object-fit: cover;
}

@media (max-width: 768px) {
  .create-activity {
    padding: 10px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .image-uploader :deep(.el-upload) {
    width: 100%;
    max-width: 300px;
  }
}
</style>