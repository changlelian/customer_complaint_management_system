<template>
  <div class="management-page">
    <div class="page-header">
      <div>
        <h2>权限管理</h2>
        <p class="text-muted text-sm mt-1">管理用户、分配角色及项目访问权限</p>
      </div>
      <button @click="openCreateModal" class="btn btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>
        新建用户
      </button>
    </div>

    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>用户名</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>关联项目</th>
            <th class="text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="font-medium">{{ user.username }}</td>
            <td class="text-muted">{{ user.email || '-' }}</td>
            <td>
              <span v-if="user.is_superuser" class="badge badge-purple">管理员</span>
              <template v-else-if="user.groups && user.groups.length > 0">
                <span v-for="group in user.groups" :key="group.id" class="badge badge-blue">{{ group.name }}</span>
              </template>
              <span v-else class="badge badge-gray">普通用户</span>
            </td>
            <td>
              <span v-if="user.assigned_projects && user.assigned_projects.length > 0" class="project-count">
                {{ user.assigned_projects.length }} 个项目
              </span>
              <span v-else class="text-muted">-</span>
            </td>
            <td class="text-right">
              <div class="action-group">
                <button @click="openEditModal(user)" class="btn btn-secondary btn-sm">编辑</button>
                <button v-if="!user.is_superuser" @click="deleteUser(user.id)" class="btn btn-danger btn-sm">删除</button>
              </div>
            </td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="5" class="empty-state">
              暂无用户数据
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 编辑/新建弹窗 -->
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑用户' : '新建用户' }}</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        
        <form @submit.prevent="saveUser">
          <div class="modal-body">
            <div class="form-grid">
              <div class="form-group">
                <label>用户名</label>
                <input v-model="formUser.username" required :disabled="isEditing" placeholder="登录用户名" />
              </div>

              <div class="form-group" v-if="!isEditing">
                <label>密码</label>
                <input v-model="formUser.password" type="password" required placeholder="登录密码" />
              </div>
            </div>

            <div class="form-group">
              <label>邮箱</label>
              <input v-model="formUser.email" type="email" placeholder="example@company.com" />
            </div>

            <div class="form-group">
              <label>角色分配</label>
              <div class="checkbox-group">
                <label v-for="group in availableGroups" :key="group.id" class="checkbox-label">
                  <input 
                    type="checkbox" 
                    :value="group.id" 
                    v-model="selectedGroups"
                  >
                  <span>{{ group.name }}</span>
                </label>
                <div v-if="availableGroups.length === 0" class="text-muted text-sm">暂无可用角色组</div>
              </div>
            </div>

            <div class="form-group">
              <label>项目权限</label>
              <div class="project-select-list">
                <label v-for="project in availableProjects" :key="project.id" class="project-item">
                  <input 
                    type="checkbox" 
                    :value="project.id" 
                    v-model="selectedProjects"
                  >
                  <span class="project-name">{{ project.name }}</span>
                  <span class="project-code">{{ project.code }}</span>
                </label>
                <div v-if="availableProjects.length === 0" class="text-muted text-sm p-2">暂无可用项目</div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">保存更改</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      users: [],
      availableGroups: [],
      availableProjects: [],
      isModalOpen: false,
      isEditing: false,
      formUser: {
        id: null,
        username: '',
        password: '',
        email: ''
      },
      selectedGroups: [],
      selectedProjects: []
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [usersRes, groupsRes, projectsRes] = await Promise.all([
          api.get('users/'),
          api.get('users/groups/'),
          api.get('projects/')
        ]);
        this.users = usersRes.data;
        this.availableGroups = groupsRes.data;
        this.availableProjects = projectsRes.data;
      } catch (err) {
        console.error('加载数据失败', err);
      }
    },
    openCreateModal() {
      this.isEditing = false;
      this.formUser = { username: '', password: '', email: '' };
      this.selectedGroups = [];
      this.selectedProjects = [];
      this.isModalOpen = true;
    },
    openEditModal(user) {
      this.isEditing = true;
      this.formUser = { ...user };
      // Initialize selected groups
      this.selectedGroups = user.groups.map(g => g.id);
      // Initialize selected projects
      this.selectedProjects = user.assigned_projects || [];
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
      this.formUser = { id: null, username: '', password: '', email: '' };
    },
    async saveUser() {
      try {
        const payload = {
          email: this.formUser.email,
          group_ids: this.selectedGroups,
          assigned_projects: this.selectedProjects
        };

        if (this.isEditing) {
          await api.patch(`users/${this.formUser.id}/`, payload);
        } else {
          payload.username = this.formUser.username;
          payload.password = this.formUser.password;
          await api.post('users/', payload);
        }

        this.closeModal();
        this.fetchData(); // Refresh list
        // alert('保存成功');
      } catch (err) {
        console.error('保存失败', err);
        let errorMsg = '保存失败';
        if (err.response && err.response.data) {
            const data = err.response.data;
            // Handle DRF standard error format
            if (typeof data === 'object') {
                const messages = [];
                for (const key in data) {
                    const value = data[key];
                    const fieldName = key === 'non_field_errors' ? '' : `${key}: `;
                    const message = Array.isArray(value) ? value.join(' ') : value;
                    messages.push(`${fieldName}${message}`);
                }
                errorMsg = messages.join('\n');
            } else {
                errorMsg = String(data);
            }
        }
        alert(errorMsg);
      }
    },
    async deleteUser(id) {
      if (!confirm('确定删除该用户吗?')) return;
      try {
        await api.delete(`users/${id}/`);
        this.fetchData();
      } catch (err) {
        console.error('删除失败', err);
        alert('删除失败');
      }
    }
  }
}
</script>

<style scoped>
.management-page {
  max-width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
  margin-bottom: 4px;
}

.mt-1 { margin-top: 0.25rem; }
.text-sm { font-size: 0.875rem; }
.font-medium { font-weight: 500; }

.icon { margin-right: 8px; }

.text-right { text-align: right; }

.action-group {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
}

.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-right: 4px;
}

.badge-purple { background-color: #EDE9FE; color: #7C3AED; }
.badge-blue { background-color: #DBEAFE; color: #2563EB; }
.badge-gray { background-color: #F3F4F6; color: #4B5563; }

.project-count {
  font-size: 0.875rem;
  color: var(--text-main);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(2px);
}

.modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-muted);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-main);
  font-size: 0.9rem;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
}

.project-select-list {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
}

.project-item {
  display: flex;
  align-items: center;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.1s;
}

.project-item:hover {
  background-color: #F3F4F6;
}

.project-item input {
  width: auto;
  margin-right: 10px;
}

.project-item .project-name {
  flex: 1;
}

.project-item .project-code {
  font-size: 0.75rem;
  background-color: #F3F4F6;
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--text-muted);
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background-color: #F9FAFB;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}
</style>
