<template>
  <div class="dashboard-container">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ 'collapsed': isSidebarCollapsed }">
      <div class="brand-section">
        <div class="logo-wrapper">
            <div class="brand-logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <span class="brand-name" v-show="!isSidebarCollapsed">客诉问题管理系统</span>
        </div>
        <button class="collapse-toggle" @click="isSidebarCollapsed = !isSidebarCollapsed" title="折叠菜单">
             <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="{'rotate-180': isSidebarCollapsed}"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
      </div>

      <div class="user-profile-mini">
         <div class="avatar-circle" :title="username">{{ username.charAt(0).toUpperCase() }}</div>
         <div class="user-details" v-show="!isSidebarCollapsed">
            <span class="name">{{ username }}</span>
            <span class="role">{{ roleName }}</span>
         </div>
      </div>

      <nav class="nav-menu">
        <div class="nav-header" v-show="!isSidebarCollapsed">视图</div>
        <div class="nav-divider" v-show="isSidebarCollapsed"></div>
        
        <a href="#" class="nav-item" :class="{ active: viewMode === 'dashboard' }" @click.prevent="selectView('dashboard')" title="仪表盘">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
          <span v-show="!isSidebarCollapsed">仪表盘</span>
        </a>

        <a href="#" class="nav-item" :class="{ active: viewMode === 'list' && selectedProjectId === null }" @click.prevent="selectProject(null)" title="全部项目概览">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          <span v-show="!isSidebarCollapsed">全部项目概览</span>
        </a>

        <div class="nav-header" v-show="!isSidebarCollapsed">我的项目</div>
        <div class="nav-divider" v-show="isSidebarCollapsed"></div>

        <div v-if="loadingProjects" class="nav-loading" v-show="!isSidebarCollapsed">加载中...</div>
        <div v-else class="project-list">
             <a v-for="p in projects" :key="p.id" href="#" 
                class="nav-item" 
                :class="{ active: selectedProjectId === p.id }" 
                @click.prevent="selectProject(p.id)"
                :title="p.name">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-icon"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
              <span v-show="!isSidebarCollapsed">{{ p.name }}</span>
            </a>
            <div v-if="projects.length === 0" class="no-projects" v-show="!isSidebarCollapsed">
                暂无分配项目
            </div>
        </div>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout" title="退出登录">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x="21" y="12" x2="9" y2="12"></line></svg>
          <span v-show="!isSidebarCollapsed">退出登录</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-header">
         <div class="header-left">
            <h1 class="page-title">{{ currentProjectName }}</h1>
            <span class="breadcrumb" v-if="selectedProjectId">项目详情</span>
         </div>
         <div class="header-actions">
             <button v-if="isAdmin" class="btn btn-outline" @click="$router.push('/admin/projects')">
                管理后台
             </button>
             <button class="btn btn-outline" @click="exportComplaints" :disabled="isExporting">
                <svg v-if="!isExporting" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                {{ isExporting ? '导出中...' : '导出Excel' }}
             </button>
             <button v-if="canSubmit" class="btn btn-primary" @click="showCreateModal = true">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="btn-icon"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                登记问题
             </button>
         </div>
      </header>

      <div class="content-body">
         <!-- Stats Cards (Optional placeholder for future) -->
         <DashboardStats v-if="viewMode === 'dashboard'" />
         
         <div v-show="viewMode === 'list'" class="complaint-list-container">
            <ComplaintList ref="list" :projectId="selectedProjectId" />
         </div>
      </div>
    </main>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
        <div class="modal-wrapper">
             <div class="modal-close-bar">
                 <button class="close-icon" @click="showCreateModal = false">&times;</button>
             </div>
             <ComplaintForm @complaint-added="onComplaintAdded" :initial-project-id="selectedProjectId" />
        </div>
    </div>

  </div>
</template>

<script>
import ComplaintList from '../components/ComplaintList.vue';
import ComplaintForm from '../components/ComplaintForm.vue';
import DashboardStats from '../components/DashboardStats.vue';
import api from '../api';

export default {
  name: 'Home',
  components: { ComplaintList, ComplaintForm, DashboardStats },
  data() {
    return {
      isLoggedIn: false,
      role: null,
      username: '',
      projects: [],
      selectedProjectId: null,
      viewMode: 'dashboard', // Default to dashboard
      loadingProjects: false,
      showCreateModal: false,
      isExporting: false,
      isSidebarCollapsed: false
    };
  },
  computed: {
    canSubmit() {
      return this.role === 'field' || this.role === 'admin' || this.role === 'auditor';
    },
    isAdmin() {
      return this.role === 'admin' || this.role === 'auditor';
    },
    roleName() {
      const map = {
        'admin': '管理员',
        'field': '现场用户',
        'ordinary': '普通用户',
        'auditor': '审核用户'
      };
      return map[this.role] || '用户';
    },
    currentProjectName() {
        if (this.viewMode === 'dashboard') return '仪表盘';
        if (!this.selectedProjectId) return '所有项目概览';
        const p = this.projects.find(p => p.id === this.selectedProjectId);
        return p ? p.name : '项目详情';
    }
  },
  created() {
    this.checkLogin();
    if (this.isLoggedIn) {
        this.fetchProjects();
    }
  },
  methods: {
    checkLogin() {
      const token = localStorage.getItem('auth_token');
      if (token) {
        this.isLoggedIn = true;
        this.role = localStorage.getItem('user_role');
        const userInfo = JSON.parse(localStorage.getItem('user_info') || '{}');
        this.username = userInfo.username || 'User';
      } else {
          this.$router.push('/login');
      }
    },
    async fetchProjects() {
        try {
            this.loadingProjects = true;
            const response = await api.get('projects/');
            this.projects = response.data;
        } catch (e) {
            console.error('Failed to fetch projects', e);
        } finally {
            this.loadingProjects = false;
        }
    },
    selectProject(id) {
        this.selectedProjectId = id;
        this.viewMode = 'list';
    },
    selectView(mode) {
        this.viewMode = mode;
        this.selectedProjectId = null;
    },
    onComplaintAdded() {
        this.showCreateModal = false;
        this.refreshList();
    },
    async exportComplaints() {
        try {
            this.isExporting = true;
            const params = {};
            if (this.selectedProjectId) {
                params.project = this.selectedProjectId;
            }
            
            const response = await api.get('complaints/export/', {
                params,
                responseType: 'blob'
            });
            
            // Create download link
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            const projectName = this.currentProjectName === '所有项目概览' ? '全部项目' : this.currentProjectName;
            const date = new Date().toISOString().slice(0, 10);
            link.setAttribute('download', `${projectName}_投诉导出_${date}.xlsx`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (e) {
            console.error('Export failed full error:', e);
            
            let errorMsg = '导出失败，请重试';
            
            // Try to read the blob error message if possible
            if (e.response && e.response.data instanceof Blob) {
                 const reader = new FileReader();
                 reader.onload = () => {
                     try {
                        const errorData = JSON.parse(reader.result);
                        errorMsg = errorData.detail || errorMsg;
                        console.error('Export error detail from backend:', errorMsg);
                        alert(`导出错误: ${errorMsg}`);
                     } catch (parseError) {
                        console.error('Failed to parse error blob:', parseError);
                        alert(errorMsg);
                     }
                 };
                 reader.readAsText(e.response.data);
            } else {
                if (e.response && e.response.data && e.response.data.detail) {
                    errorMsg = e.response.data.detail;
                } else if (e.message) {
                    errorMsg = e.message;
                }
                console.error('Export error message:', errorMsg);
                alert(`导出错误: ${errorMsg}`);
            }
        } finally {
            this.isExporting = false;
        }
    },
    refreshList() {
      if (this.$refs.list) {
        this.$refs.list.fetchComplaints();
      }
    },
    logout() {
      if(confirm('确定要退出登录吗？')) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_info');
        this.$router.push('/login');
      }
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  display: flex;
  height: 100vh;
  background-color: var(--bg-body);
  overflow: hidden;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background-color: var(--bg-surface);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  z-index: 20;
  box-shadow: var(--shadow-sm);
  transition: width 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.sidebar.collapsed {
  width: 70px;
}

.brand-section {
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px 0 24px;
    border-bottom: 1px solid var(--border-color);
    gap: 12px;
    white-space: nowrap;
}

.sidebar.collapsed .brand-section {
    padding: 0;
    justify-content: center;
}

.logo-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    overflow: hidden;
}

.sidebar.collapsed .logo-wrapper {
    display: none;
}

.collapse-toggle {
    background: transparent;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.sidebar.collapsed .collapse-toggle {
    width: 100%;
    height: 100%;
    border-radius: 0;
}

.collapse-toggle:hover {
    background-color: var(--bg-body);
    color: var(--text-main);
}

.rotate-180 {
    transform: rotate(180deg);
}

.brand-logo {
    color: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.brand-name {
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--text-main);
    letter-spacing: -0.01em;
}

.user-profile-mini {
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid var(--border-color);
    background-color: #FAFAFA;
    overflow: hidden;
    white-space: nowrap;
    transition: padding 0.3s;
}

.sidebar.collapsed .user-profile-mini {
    padding: 20px 0;
    justify-content: center;
}

.avatar-circle {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: var(--shadow-sm);
    flex-shrink: 0;
}

.user-details {
    display: flex;
    flex-direction: column;
}

.user-details .name {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-main);
}

.user-details .role {
    font-size: 0.75rem;
    color: var(--text-muted);
    background: var(--bg-body);
    padding: 2px 8px;
    border-radius: 12px;
    margin-top: 4px;
    display: inline-block;
    width: fit-content;
    border: 1px solid var(--border-color);
}

.nav-menu {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 24px 16px;
    transition: padding 0.3s;
}

.sidebar.collapsed .nav-menu {
    padding: 24px 8px;
}

.nav-header {
    font-size: 0.7rem;
    text-transform: uppercase;
    color: var(--text-light);
    font-weight: 700;
    margin-bottom: 12px;
    padding-left: 12px;
    margin-top: 24px;
    letter-spacing: 0.05em;
    white-space: nowrap;
}

.nav-divider {
    height: 1px;
    background-color: var(--border-color);
    margin: 12px 4px;
}

.nav-header:first-child {
    margin-top: 0;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    color: var(--text-secondary);
    text-decoration: none;
    border-radius: var(--radius-md);
    margin-bottom: 4px;
    transition: all 0.2s ease;
    font-size: 0.9rem;
    font-weight: 500;
    border: 1px solid transparent;
    white-space: nowrap;
    overflow: hidden;
}

.sidebar.collapsed .nav-item {
    justify-content: center;
    padding: 12px;
}

.nav-item:hover {
    background-color: var(--bg-body);
    color: var(--text-main);
}

.nav-item.active {
    background-color: var(--primary-light);
    color: var(--primary-color);
    border-color: rgba(79, 70, 229, 0.1);
}

.nav-icon {
    opacity: 0.6;
    transition: opacity 0.2s;
    flex-shrink: 0;
}

.nav-item.active .nav-icon {
    opacity: 1;
}

.no-projects {
    padding: 16px;
    font-size: 0.85rem;
    color: var(--text-light);
    text-align: center;
    font-style: italic;
}

.sidebar-footer {
    padding: 16px;
    border-top: 1px solid var(--border-color);
    background-color: var(--bg-surface);
}

.btn-logout {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 12px;
    border: 1px solid var(--border-color);
    background: white;
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}

.btn-logout:hover {
    background: var(--danger-bg);
    color: var(--danger-text);
    border-color: transparent;
}

/* Main Content */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background-color: var(--bg-body);
}

.top-header {
    height: 70px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 32px;
    position: sticky;
    top: 0;
    z-index: 10;
}

.header-left {
    display: flex;
    flex-direction: column;
}

.page-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-main);
    margin: 0;
}

.breadcrumb {
    font-size: 0.85rem;
    color: var(--text-light);
    margin-top: 2px;
}

.header-actions {
    display: flex;
    gap: 12px;
}

.btn {
    padding: 0.6rem 1.2rem;
    border-radius: var(--radius-md);
    font-weight: 500;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
    border: 1px solid transparent;
    box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
    background-color: var(--primary-hover);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.btn-outline {
    background-color: white;
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
}

.btn-outline:hover {
    background-color: var(--bg-body);
    border-color: var(--text-muted);
}

.content-body {
    flex: 1;
    overflow-y: auto;
    padding: 32px;
}

/* Modal */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(4px);
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.2s ease-out;
}

.modal-wrapper {
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    background: white;
    border-radius: var(--radius-lg);
    position: relative;
    box-shadow: var(--shadow-lg);
    animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-close-bar {
    position: absolute;
    top: 16px;
    right: 16px;
    z-index: 10;
}

.close-icon {
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    transition: all 0.2s;
    box-shadow: var(--shadow-sm);
}

.close-icon:hover {
    background-color: var(--bg-body);
    color: var(--text-main);
    transform: rotate(90deg);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>