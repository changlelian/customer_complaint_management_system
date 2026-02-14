<template>
  <div class="admin-layout">
    <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
      <div class="sidebar-header">
        <div class="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
        </div>
        <div class="logo-text" v-show="!isCollapsed">客诉问题管理系统</div>
        <button class="collapse-toggle" @click="isCollapsed = !isCollapsed">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="{'rotate-180': isCollapsed}"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
      </div>
      
      <nav class="nav-menu">
        <div v-if="['admin', 'auditor'].includes(userRole)" class="nav-section-title" v-show="!isCollapsed">系统管理</div>
        <div v-if="['admin', 'auditor'].includes(userRole) && isCollapsed" class="nav-divider"></div>

        <router-link v-if="userRole === 'admin'" to="/admin/projects" class="nav-item" :title="isCollapsed ? '项目管理' : ''">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
          <span v-show="!isCollapsed">项目管理</span>
        </router-link>

        <router-link v-if="userRole === 'admin'" to="/admin/versions" class="nav-item" :title="isCollapsed ? '软件版本管理' : ''">
            <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
            <span v-show="!isCollapsed">软件版本管理</span>
        </router-link>
        
        <router-link v-if="['admin', 'auditor'].includes(userRole)" to="/admin/types" class="nav-item" :title="isCollapsed ? '客诉类型管理' : ''">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          <span v-show="!isCollapsed">客诉类型管理</span>
        </router-link>
        
        <router-link v-if="userRole === 'admin'" to="/admin/users" class="nav-item" :title="isCollapsed ? '权限管理' : ''">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          <span v-show="!isCollapsed">权限管理</span>
        </router-link>

        <div class="nav-divider"></div>
        <div class="nav-section-title" v-show="!isCollapsed">现场问题单管理</div>
        <div class="project-list">
          <router-link 
            v-for="project in projects" 
            :key="project.id"
            :to="'/admin/complaints/project/' + project.id" 
            class="nav-item sub-item"
            :title="isCollapsed ? project.name : ''"
          >
            <span class="project-icon-box">
                {{ project.name.charAt(0) }}
            </span>
            <span class="project-name" v-show="!isCollapsed">{{ project.name }}</span>
          </router-link>
           <div v-if="projects.length === 0" class="empty-nav" v-show="!isCollapsed">暂无项目</div>
        </div>
      </nav>

      <div class="sidebar-footer">
        <router-link to="/" class="nav-item footer-link" :title="isCollapsed ? '返回前台' : ''">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          <span v-show="!isCollapsed">返回前台</span>
        </router-link>
        
        <button @click="handleLogout" class="logout-btn" :title="isCollapsed ? '退出登录' : ''">
          <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          <span v-show="!isCollapsed">退出登录</span>
        </button>
      </div>
    </div>
    
    <div class="main-content">
      <header class="top-bar">
        <div class="breadcrumbs">
          <span class="text-muted">管理后台</span>
          <span class="separator">/</span>
          <span class="current-page">{{ currentRouteName }}</span>
        </div>
        <div class="user-profile">
          <div class="avatar">A</div>
          <span class="username">管理员</span>
        </div>
      </header>
      <div class="content-wrapper">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: 'AdminLayout',
  data() {
    return {
      projects: [],
      userRole: localStorage.getItem('user_role') || 'ordinary',
      isCollapsed: false
    };
  },
  computed: {
    currentRouteName() {
      if (this.$route.path.includes('/admin/complaints/project/')) {
        return '现场问题单管理';
      }
      const map = {
        'projects': '项目管理',
        'types': '客诉类型管理',
        'versions': '软件版本管理',
        'users': '权限管理'
      };
      const path = this.$route.path.split('/').pop();
      return map[path] || '概览';
    }
  },
  created() {
    this.fetchProjects();
    window.addEventListener('project-update', this.fetchProjects);
  },
  beforeUnmount() {
    window.removeEventListener('project-update', this.fetchProjects);
  },
  methods: {
    async fetchProjects() {
      try {
        const response = await api.get('projects/');
        this.projects = response.data;
      } catch (err) {
        console.error('Failed to load projects for menu', err);
      }
    },
    handleLogout() {
      if(confirm('确定要退出登录吗？')) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_role');
        this.$router.push('/login');
      }
    }
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  background-color: #f1f5f9; /* Slate 100 */
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.sidebar {
  width: 280px;
  background: #0f172a; /* Slate 900 */
  color: #94a3b8; /* Slate 400 */
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 24px rgba(0,0,0,0.1);
  z-index: 50;
  transition: width 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.sidebar.collapsed {
  width: 72px;
}

.sidebar-header {
  height: 72px;
  display: flex;
  align-items: center;
  padding: 0 16px 0 24px;
  background-color: #1e293b; /* Slate 800 */
  border-bottom: 1px solid #334155; /* Slate 700 */
  justify-content: space-between;
}

.sidebar.collapsed .sidebar-header {
  padding: 0;
  justify-content: center;
}

.sidebar.collapsed .logo-icon {
  display: none;
}

.collapse-toggle {
    background: transparent;
    border: none;
    color: #94a3b8;
    cursor: pointer;
    padding: 6px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.collapse-toggle:hover {
    background-color: rgba(255,255,255,0.1);
    color: white;
}

.sidebar.collapsed .collapse-toggle {
    width: 100%;
    height: 100%;
    border-radius: 0;
}

.rotate-180 {
    transform: rotate(180deg);
}

.logo-icon {
  color: #38bdf8; /* Sky 400 */
  margin-right: 12px;
  display: flex;
}

.logo-text {
  font-size: 1rem;
  font-weight: 700;
  color: #f8fafc; /* Slate 50 */
  letter-spacing: 0.5px;
}

.nav-menu {
  flex: 1;
  padding: 24px 16px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 4px;
  color: #94a3b8;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 0.9rem;
}

.nav-item:hover {
  background-color: #1e293b;
  color: #f8fafc;
}

.nav-item.router-link-active {
  background-color: #3b82f6; /* Blue 500 */
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.nav-item .icon {
  margin-right: 12px;
  opacity: 0.8;
}

.nav-divider {
  height: 1px;
  background-color: #334155;
  margin: 24px 0 16px 0;
}

.nav-section-title {
  padding: 0 16px;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #64748b; /* Slate 500 */
  font-weight: 700;
  margin-bottom: 12px;
  margin-top: 8px;
  letter-spacing: 0.05em;
}

.sub-item {
  padding-left: 16px;
}

.project-icon-box {
    width: 24px;
    height: 24px;
    background-color: #334155;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    color: #e2e8f0;
    margin-right: 12px;
    transition: background-color 0.2s;
}

.sub-item:hover .project-icon-box, .sub-item.router-link-active .project-icon-box {
  background-color: rgba(255,255,255,0.2);
  color: white;
}

.project-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-nav {
  padding: 10px 16px;
  font-size: 0.85rem;
  color: #64748b;
  font-style: italic;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #334155;
  background-color: #0f172a;
}

.footer-link {
  margin-bottom: 8px;
  color: #94a3b8;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: none;
  border: 1px solid #334155;
  color: #ef4444; /* Red 500 */
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.9rem;
  font-weight: 500;
}

.logout-btn:hover {
  background-color: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

.logout-btn .icon {
  margin-right: 12px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f8fafc;
}

.top-bar {
  height: 72px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  border-bottom: 1px solid #e2e8f0;
  z-index: 10;
}

.breadcrumbs {
  font-size: 0.95rem;
  color: #64748b;
  display: flex;
  align-items: center;
}

.breadcrumbs .separator {
  margin: 0 10px;
  color: #cbd5e1;
}

.breadcrumbs .current-page {
  color: #0f172a;
  font-weight: 600;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 30px;
  transition: background-color 0.2s;
}

.user-profile:hover {
    background-color: #f1f5f9;
}

.avatar {
  width: 32px;
  height: 32px;
  background-color: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  margin-right: 12px;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.username {
  font-weight: 500;
  color: #334155;
  font-size: 0.9rem;
}

.content-wrapper {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
}

.sidebar.collapsed .nav-menu {
    padding: 24px 8px;
}

.sidebar.collapsed .nav-item {
    justify-content: center;
    padding: 12px;
}

.sidebar.collapsed .nav-item .icon {
    margin-right: 0;
}

.sidebar.collapsed .sub-item {
    padding-left: 0;
}

.sidebar.collapsed .project-icon-box {
    margin-right: 0;
}

.sidebar.collapsed .logout-btn {
    justify-content: center;
    padding: 12px;
}

.sidebar.collapsed .logout-btn .icon {
    margin-right: 0;
}
</style>
