<template>
  <div class="version-list-page">
    <div class="page-header">
      <h2>软件版本管理</h2>
      <button @click="showAddModal = true" class="btn btn-primary" :disabled="!selectedProject">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        添加新版本
      </button>
    </div>

    <div class="filter-section">
      <div class="form-group">
        <label>选择项目:</label>
        <select v-model="selectedProject" @change="fetchVersions" class="form-select project-select">
            <option :value="null" disabled>请选择项目</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
        <div class="spinner"></div> 加载中...
    </div>

    <div v-else-if="!selectedProject" class="empty-state">
      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon text-gray-400"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
      <p>请先选择一个项目以管理其软件版本</p>
    </div>

    <div v-else-if="versions.length === 0" class="empty-state">
        <p>该项目暂无版本记录</p>
    </div>

    <div v-else class="table-container card">
      <table class="data-table">
        <thead>
          <tr>
            <th>版本号</th>
            <th>创建时间</th>
            <th class="text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="version in versions" :key="version.id">
            <td class="font-medium">{{ version.version_number }}</td>
            <td class="text-gray-500">{{ formatDate(version.created_at) }}</td>
            <td class="text-right">
              <button @click="deleteVersion(version)" class="btn-text text-danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Version Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>添加新版本</h3>
          <button class="close-btn" @click="showAddModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addVersion">
            <div class="form-group">
              <label>所属项目</label>
              <input :value="selectedProjectName" disabled class="form-input bg-gray-100" />
            </div>
            <div class="form-group">
              <label>版本号</label>
              <input v-model="newVersionNumber" required placeholder="例如: v1.0.0" class="form-input" ref="versionInput" />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showAddModal = false">取消</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                {{ submitting ? '提交中...' : '确认添加' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'VersionList',
  data() {
    return {
      projects: [],
      selectedProject: null,
      versions: [],
      loading: false,
      showAddModal: false,
      newVersionNumber: '',
      submitting: false
    };
  },
  computed: {
    selectedProjectName() {
        const p = this.projects.find(p => p.id === this.selectedProject);
        return p ? p.name : '';
    }
  },
  created() {
    this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
        try {
            const response = await api.get('projects/');
            this.projects = response.data;
            if (this.projects.length > 0) {
                // Optionally select first project? Or let user select.
                // Let's let user select.
            }
        } catch (err) {
            console.error(err);
        }
    },
    async fetchVersions() {
        if (!this.selectedProject) return;
        this.loading = true;
        try {
            const response = await api.get(`versions/?project=${this.selectedProject}`);
            this.versions = response.data;
        } catch (err) {
            console.error(err);
            alert('获取版本列表失败');
        } finally {
            this.loading = false;
        }
    },
    async addVersion() {
        if (!this.newVersionNumber.trim()) return;
        this.submitting = true;
        try {
            await api.post('versions/', {
                project: this.selectedProject,
                version_number: this.newVersionNumber
            });
            this.newVersionNumber = '';
            this.showAddModal = false;
            this.fetchVersions();
            alert('添加成功');
        } catch (err) {
            alert('添加失败: ' + (err.response?.data?.detail || err.message));
        } finally {
            this.submitting = false;
        }
    },
    async deleteVersion(version) {
        if (!confirm(`确定要删除版本 ${version.version_number} 吗？`)) return;
        try {
            await api.delete(`versions/${version.id}/`);
            this.fetchVersions();
        } catch (err) {
            alert('删除失败');
        }
    },
    formatDate(dateString) {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleString('zh-CN');
    }
  },
  watch: {
      showAddModal(val) {
          if (val) {
              this.$nextTick(() => {
                  if (this.$refs.versionInput) this.$refs.versionInput.focus();
              });
          }
      }
  }
};
</script>

<style scoped>
.version-list-page {
  padding: 24px;
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
}

.filter-section {
    margin-bottom: 24px;
    background: white;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.project-select {
    max-width: 300px;
}

.table-container {
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    overflow: hidden;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th, .data-table td {
    padding: 12px 24px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.data-table th {
    background-color: #f8fafc;
    font-weight: 600;
    color: var(--text-secondary);
}

.empty-state {
    text-align: center;
    padding: 48px;
    color: var(--text-secondary);
    background: white;
    border-radius: 8px;
}

.empty-icon {
    margin-bottom: 16px;
    color: #cbd5e1;
}
</style>