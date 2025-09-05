<template>
  <div class="profile">
    <el-card class="profile-card">
      <div class="profile-header">
        <div class="avatar-section">
          <el-avatar :size="80" :src="userInfo.avatar" class="user-avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <el-button type="text" @click="showAvatarDialog = true">更换头像</el-button>
        </div>
        <div class="user-basic-info">
          <h2>{{ userInfo.real_name || userInfo.username }}</h2>
          <p class="user-role">{{ getRoleText(userInfo.role) }}</p>
          <p class="volunteer-hours">累计志愿时长：{{ userInfo.volunteer_hours || 0 }}小时</p>
        </div>
      </div>
    </el-card>

    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
          <el-button v-if="!editing" type="primary" @click="startEdit">编辑</el-button>
          <div v-else>
            <el-button @click="cancelEdit">取消</el-button>
            <el-button type="primary" @click="saveProfile" :loading="loading">保存</el-button>
          </div>
        </div>
      </template>

      <el-form :model="profileForm" :rules="rules" ref="profileFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="profileForm.username" :disabled="true" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" :disabled="!editing" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="真实姓名" prop="real_name">
              <el-input v-model="profileForm.real_name" :disabled="!editing" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="profileForm.phone" :disabled="!editing" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="个人简介">
          <el-input 
            v-model="profileForm.bio" 
            type="textarea" 
            :rows="4" 
            :disabled="!editing"
            placeholder="请输入个人简介"
          />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="form-card">
      <template #header>
        <span>修改密码</span>
      </template>
      
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input v-model="passwordForm.currentPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changePassword" :loading="passwordLoading">
            修改密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 头像上传对话框 -->
    <el-dialog v-model="showAvatarDialog" title="更换头像" width="400px">
      <el-upload
        class="avatar-uploader"
        action="#"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload"
        :http-request="uploadAvatar"
      >
        <img v-if="newAvatarUrl" :src="newAvatarUrl" class="avatar-preview" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>
      <template #footer>
        <el-button @click="showAvatarDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmAvatar" :disabled="!newAvatarUrl">
          确认
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { User, Plus } from '@element-plus/icons-vue'

export default {
  name: 'Profile',
  components: {
    User,
    Plus
  },
  data() {
    return {
      editing: false,
      loading: false,
      passwordLoading: false,
      showAvatarDialog: false,
      newAvatarUrl: '',
      profileForm: {
        username: '',
        email: '',
        real_name: '',
        phone: '',
        bio: ''
      },
      originalProfile: {},
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      rules: {
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
        ],
        real_name: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        phone: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      passwordRules: {
        currentPassword: [
          { required: true, message: '请输入当前密码', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少6位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认新密码', trigger: 'blur' },
          { validator: this.validateConfirmPassword, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapState('auth', ['userInfo'])
  },
  created() {
    this.initProfileForm()
  },
  methods: {
    ...mapActions('auth', ['updateProfile', 'changeUserPassword']),
    initProfileForm() {
      this.profileForm = {
        username: this.userInfo.username || '',
        email: this.userInfo.email || '',
        real_name: this.userInfo.real_name || '',
        phone: this.userInfo.phone || '',
        bio: this.userInfo.bio || ''
      }
      this.originalProfile = { ...this.profileForm }
    },
    startEdit() {
      this.editing = true
    },
    cancelEdit() {
      this.editing = false
      this.profileForm = { ...this.originalProfile }
      this.$refs.profileFormRef?.clearValidate()
    },
    async saveProfile() {
      try {
        await this.$refs.profileFormRef.validate()
        this.loading = true
        
        await this.updateProfile(this.profileForm)
        this.$message.success('个人信息更新成功！')
        this.editing = false
        this.originalProfile = { ...this.profileForm }
      } catch (error) {
        if (error.message) {
          this.$message.error(error.message)
        }
      } finally {
        this.loading = false
      }
    },
    async changePassword() {
      try {
        await this.$refs.passwordFormRef.validate()
        this.passwordLoading = true
        
        await this.changeUserPassword({
          currentPassword: this.passwordForm.currentPassword,
          newPassword: this.passwordForm.newPassword
        })
        
        this.$message.success('密码修改成功！')
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
        this.$refs.passwordFormRef.resetFields()
      } catch (error) {
        this.$message.error(error.message || '密码修改失败')
      } finally {
        this.passwordLoading = false
      }
    },
    validateConfirmPassword(rule, value, callback) {
      if (value !== this.passwordForm.newPassword) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('头像只能是 JPG/PNG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('头像大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    uploadAvatar(options) {
      // 这里应该上传到服务器，暂时使用本地预览
      const reader = new FileReader()
      reader.onload = (e) => {
        this.newAvatarUrl = e.target.result
      }
      reader.readAsDataURL(options.file)
    },
    confirmAvatar() {
      // 这里应该调用API更新头像
      this.$message.success('头像更新成功！')
      this.showAvatarDialog = false
      this.newAvatarUrl = ''
    },
    getRoleText(role) {
      const roleMap = {
        'volunteer': '志愿者',
        'organizer': '组织者',
        'admin': '管理员'
      }
      return roleMap[role] || '志愿者'
    }
  }
}
</script>

<style scoped>
.profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-card {
  margin-bottom: 20px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  background-color: #f5f7fa;
}

.user-basic-info h2 {
  margin: 0 0 10px 0;
  color: #303133;
}

.user-role {
  color: #909399;
  margin: 0 0 5px 0;
}

.volunteer-hours {
  color: #67c23a;
  font-weight: bold;
  margin: 0;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.avatar-uploader {
  display: flex;
  justify-content: center;
}

.avatar-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: 0.2s;
  width: 178px;
  height: 178px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-uploader :deep(.el-upload:hover) {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.avatar-preview {
  width: 178px;
  height: 178px;
  object-fit: cover;
}

@media (max-width: 768px) {
  .profile {
    padding: 10px;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .card-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
}
</style>