<template>
  <div class="project-complaints-page">
    <div class="page-header">
      <div class="header-left">
        <h2>{{ projectName || '项目投诉管理' }}</h2>
        <span v-if="projectCode" class="project-code">{{ projectCode }}</span>
      </div>
      <div class="header-actions">
        <button v-if="['admin'].includes(userRole)" @click="openVersionManager" class="btn btn-secondary" style="margin-right: 12px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
            版本管理
        </button>
        <button v-if="['field', 'auditor', 'admin'].includes(userRole)" @click="showForm = true" class="btn btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            登记新问题
        </button>
      </div>
    </div>

    <!-- Filters & Toolbar -->
    <div class="filter-panel">
      <div class="filter-header">
        <div class="filter-title-group">
            <div class="filter-icon-box">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
            </div>
            <h3>筛选查询</h3>
        </div>
        <div class="filter-actions">
           <button @click="resetFilters" class="btn btn-light" title="重置筛选">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
            重置
           </button>
           <button @click="fetchComplaints($route.params.id)" class="btn btn-primary">
             <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 4v6h-6"></path><path d="M1 20v-6h6"></path><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
             刷新
            </button>
        </div>
      </div>
      
      <div class="filter-content">
         <div class="filter-row">
             <div class="filter-group">
                <label>状态</label>
                <select v-model="filterStatus" @change="handleFilterChange" class="modern-select">
                    <option value="">全部状态</option>
                    <option value="pending">待处理</option>
                    <option value="in_progress">处理中</option>
                    <option value="resolved">已解决</option>
                </select>
             </div>
             <div class="filter-group">
                <label>类型</label>
                <select v-model="filterType" @change="handleFilterChange" class="modern-select">
                    <option value="">全部类型</option>
                    <option v-for="type in complaintTypes" :key="type.id" :value="type.id">
                      {{ type.name }}
                    </option>
                </select>
             </div>
             <div class="filter-group">
                <label>客户现场</label>
                <div class="input-with-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="field-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                    <input v-model="filterCustomer" @change="handleFilterChange" placeholder="输入客户名称..." class="modern-input" />
                </div>
             </div>
             <div class="filter-group">
                <label>登记人</label>
                <div class="input-with-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="field-icon"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><line x1="19" y1="8" x2="19" y2="14"></line><line x1="22" y1="11" x2="16" y2="11"></line></svg>
                    <input v-model="filterRegistrant" @change="handleFilterChange" placeholder="输入登记人..." class="modern-input" />
                </div>
             </div>
             <div class="filter-group wide">
                <label>提交时间</label>
                <div class="date-range-wrapper">
                    <input type="date" v-model="filterStartDate" @change="handleFilterChange" class="modern-input date-input" />
                    <span class="range-separator">至</span>
                    <input type="date" v-model="filterEndDate" @change="handleFilterChange" class="modern-input date-input" />
                </div>
             </div>
         </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="skeleton-loader">
          <div class="skeleton-header"></div>
          <div class="skeleton-row" v-for="i in 5" :key="i"></div>
      </div>
    </div>

    <div v-else-if="error" class="error-state">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="complaints.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <p>该项目暂无投诉记录</p>
      </div>

      <div v-else class="complaints-table-container">
        <table class="complaints-table">
          <thead>
            <tr>
              <th>编号</th>
              <th>标题</th>
              <th>客户现场</th>
              <th>类型</th>
              <th>登记人</th>
              <th>状态</th>
              <th>提交时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="complaint in complaints" :key="complaint.id">
              <td class="font-mono text-gray-600">{{ complaint.complaint_code || '-' }}</td>
              <td>
                 <div class="complaint-title" :title="complaint.title">{{ complaint.title }}</div>
              </td>
              <td :title="complaint.customer_name">{{ complaint.customer_name }}</td>
              <td>
                  <span class="type-tag">{{ complaint.type_name || '未分类' }}</span>
              </td>
              <td>{{ complaint.registrant_name || '-' }}</td>
              <td>
                <span :class="['status-badge', complaint.status]">
                  {{ formatStatus(complaint.status) }}
                </span>
              </td>
              <td class="text-gray-500 text-sm">{{ formatDate(complaint.created_at) }}</td>
              <td>
                <button class="btn-text" @click="viewDetails(complaint)">详情</button>
                <button v-if="canEditComplaint(complaint)" class="btn-text" @click="editComplaint(complaint)" style="margin-left: 8px;">编辑</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showForm" class="modal-overlay" @click.self="handleFormCancel">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingComplaint ? '编辑问题' : '登记新问题' }}</h3>
          <button class="close-btn" @click="handleFormCancel">&times;</button>
        </div>
        <div class="modal-body">
          <ComplaintForm 
            :initial-project-id="$route.params.id"
            :initial-data="editingComplaint"
            :is-edit="!!editingComplaint"
            @submit-success="handleFormSuccess"
            @cancel="handleFormCancel"
          />
        </div>
      </div>
    </div>

    <!-- View Details Modal (Improved version) -->
    <div v-if="selectedComplaint" class="modal-overlay" @click.self="selectedComplaint = null">
      <div class="modal-content large-modal">
        <div class="modal-header">
          <h3>问题详情</h3>
          <div class="header-actions">
              <button v-if="canEditComplaint(selectedComplaint)" @click="editComplaint(selectedComplaint)" class="btn btn-secondary btn-sm" style="margin-right: 12px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                编辑
              </button>
              <button class="close-btn" @click="selectedComplaint = null">&times;</button>
          </div>
        </div>
        <div class="modal-body detail-view">
          <!-- Info Grid -->
          <div class="detail-grid">
            <div class="detail-item full-width">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                 标题
              </span>
              <span class="detail-value title-value">{{ selectedComplaint.title }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                 状态
              </span>
              <span :class="['status-badge', selectedComplaint.status]">
                {{ formatStatus(selectedComplaint.status) }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><line x1="19" y1="8" x2="19" y2="14"></line><line x1="22" y1="11" x2="16" y2="11"></line></svg>
                 客户
              </span>
              <span class="detail-value">{{ selectedComplaint.customer_name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                 类型
              </span>
              <span class="detail-value">{{ selectedComplaint.type_name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                 分类
              </span>
              <span class="detail-value">{{ selectedComplaint.category_display }}</span>
            </div>
            <div class="detail-item" v-if="selectedComplaint.software_version_number">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
                 软件版本
              </span>
              <span class="detail-value">{{ selectedComplaint.software_version_number }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                 登记人
              </span>
              <span class="detail-value">{{ selectedComplaint.registrant_name }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                 提交时间
              </span>
              <span class="detail-value">{{ formatDate(selectedComplaint.created_at) }}</span>
            </div>
          </div>

          <div class="detail-group">
            <span class="detail-label">问题描述</span>
            <div class="detail-text ql-snow">
              <div class="ql-editor" v-html="selectedComplaint.description"></div>
            </div>
          </div>

          <div class="detail-row" v-if="selectedComplaint.attachment">
            <span class="detail-label">附件:</span>
            <a :href="selectedComplaint.attachment" target="_blank" class="attachment-link">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
                下载附件
            </a>
          </div>

          <!-- Comments Section -->
          <div class="detail-section comments-section">
            <div class="section-title">备注 / 评论</div>
            
            <div class="comments-container">
                <div class="comments-list" v-if="comments.length > 0">
                    <div v-for="comment in comments" :key="comment.id" class="comment-item">
                        <div class="comment-header">
                            <span class="comment-user">{{ comment.user_name }}</span>
                            <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                        </div>
                        <div class="comment-content">{{ comment.content }}</div>
                        <div v-if="comment.image" class="comment-image-container">
                            <a :href="comment.image" target="_blank">
                                <img :src="comment.image" alt="评论图片" class="comment-image-preview">
                            </a>
                        </div>
                    </div>
                </div>
                <div v-else class="no-comments">暂无备注</div>
            </div>

            <div class="add-comment">
                <textarea 
                    v-model="newComment" 
                    placeholder="添加备注..." 
                    class="form-textarea"
                    rows="3"
                ></textarea>
                <div class="comment-tools">
                    <input type="file" @change="handleCommentImageChange" class="comment-image-input" accept="image/*" id="comment-image-upload">
                    <label for="comment-image-upload" class="image-upload-btn" title="上传图片">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                        <span v-if="newCommentImage" class="file-name">{{ newCommentImage.name }}</span>
                    </label>
                    <button 
                        @click="submitComment" 
                        class="btn btn-primary btn-sm"
                        :disabled="(!newComment.trim() && !newCommentImage) || submittingComment"
                    >
                        {{ submittingComment ? '提交中...' : '发送' }}
                    </button>
                </div>
            </div>
          </div>
        </div>
        <div class="modal-footer footer-spaced">
           <div class="left-actions">
               <div v-if="['auditor', 'admin'].includes(userRole)" class="audit-actions" style="display: inline-block; margin-right: 10px;">
                   <button v-if="selectedComplaint.status === 'pending'" @click="updateStatus(selectedComplaint, 'in_progress')" class="btn btn-warning">开始处理</button>
                   <button v-if="selectedComplaint.status !== 'resolved'" @click="updateStatus(selectedComplaint, 'resolved')" class="btn btn-success">已解决</button>
                   <button v-if="selectedComplaint.status === 'resolved'" @click="updateStatus(selectedComplaint, 'in_progress')" class="btn btn-warning">重开</button>
               </div>
               <button v-if="canEditComplaint(selectedComplaint)" @click="editComplaint(selectedComplaint)" class="btn btn-secondary">编辑</button>
           </div>
           <button class="btn btn-primary" @click="selectedComplaint = null">关闭</button>
        </div>
      </div>
    </div>

    <div v-if="showVersionManager" class="modal-overlay" @click.self="showVersionManager = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>版本管理</h3>
          <button class="close-btn" @click="showVersionManager = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="add-version-row" style="display: flex; gap: 10px; margin-bottom: 20px;">
            <input v-model="newVersion" placeholder="输入新版本号 (e.g. v1.0.0)" class="form-input" style="flex: 1;" />
            <button @click="addVersion" class="btn btn-primary" :disabled="!newVersion.trim() || addingVersion">
              {{ addingVersion ? '添加中...' : '添加' }}
            </button>
          </div>
          
          <div class="versions-list">
             <div v-if="versions.length === 0" class="empty-text" style="text-align: center; color: #666;">暂无版本记录</div>
             <div v-else v-for="v in versions" :key="v.id" class="version-item" style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee;">
               <div>
                   <span class="version-number" style="font-weight: 500;">{{ v.version_number }}</span>
                   <span class="version-date" style="margin-left: 10px; color: #888; font-size: 0.9em;">{{ formatDate(v.created_at) }}</span>
               </div>
               <button @click="deleteVersion(v.id)" class="btn-text text-danger" title="删除">删除</button>
             </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '../api';
import ComplaintForm from '../components/ComplaintForm.vue';
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';

export default {
  name: 'ProjectComplaints',
  components: {
    QuillEditor,
    ComplaintForm
  },
  data() {
    return {
      complaints: [],
      complaintTypes: [],
      versions: [], // New: Store versions
      loading: true,
      error: null,
      projectName: '',
      projectCode: '',
      showForm: false,
      showVersionManager: false, // New: Version manager modal
      addingVersion: false, // New: Loading state for adding version
      newVersion: '', // New: Input for new version
      selectedComplaint: null,
      editingComplaint: null,
      userRole: localStorage.getItem('user_role') || 'ordinary',
      filterStatus: '',
      filterType: '',
      filterCustomer: '',
      filterRegistrant: '',
      filterStartDate: '',
      filterEndDate: '',
      currentComplaint: null,
      comments: [],
      newComment: '',
      newCommentImage: null,
      submittingComment: false
    };
  },
  created() {
    this.fetchComplaintTypes();
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchProjectDetails(newId);
          this.fetchComplaints(newId);
          this.fetchVersions(newId); // New: Fetch versions
        }
      }
    }
  },
  methods: {
    async fetchVersions(projectId) {
        try {
            const response = await api.get(`versions/?project=${projectId}`);
            this.versions = response.data;
        } catch (err) {
            console.error('无法加载版本列表', err);
        }
    },
    openVersionManager() {
        this.showVersionManager = true;
        this.fetchVersions(this.$route.params.id);
    },
    async addVersion() {
        if (!this.newVersion.trim()) return;
        this.addingVersion = true;
        try {
            await api.post('versions/', {
                project: this.$route.params.id,
                version_number: this.newVersion
            });
            this.newVersion = '';
            this.fetchVersions(this.$route.params.id);
        } catch (err) {
            alert('添加版本失败: ' + (err.response?.data?.detail || err.message));
        } finally {
            this.addingVersion = false;
        }
    },
    async deleteVersion(id) {
        if (!confirm('确定删除此版本吗？')) return;
        try {
            await api.delete(`versions/${id}/`);
            this.fetchVersions(this.$route.params.id);
        } catch (err) {
            alert('删除失败');
        }
    },
    async fetchComplaintTypes() {
      try {
        const response = await api.get('types/');
        this.complaintTypes = response.data;
      } catch (err) {
        console.error('无法加载客诉类型', err);
      }
    },
    async fetchProjectDetails(id) {
      try {
        const response = await api.get(`projects/${id}/`);
        this.projectName = response.data.name;
        this.projectCode = response.data.code;
      } catch (err) {
        console.error('无法加载项目详情', err);
      }
    },
    async fetchComplaints(projectId) {
      this.loading = true;
      try {
        let url = `complaints/?project=${projectId}`;
        if (this.filterStatus) {
            url += `&status=${this.filterStatus}`;
        }
        if (this.filterType) {
            url += `&type=${this.filterType}`;
        }
        if (this.filterCustomer) {
            url += `&customer_name=${encodeURIComponent(this.filterCustomer)}`;
        }
        if (this.filterRegistrant) {
            url += `&registrant_name=${encodeURIComponent(this.filterRegistrant)}`;
        }
        if (this.filterStartDate) {
            url += `&start_date=${this.filterStartDate}`;
        }
        if (this.filterEndDate) {
            url += `&end_date=${this.filterEndDate}`;
        }
        const response = await api.get(url);
        this.complaints = response.data;
      } catch (err) {
        this.error = '无法加载投诉列表';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    handleFilterChange() {
        this.fetchComplaints(this.$route.params.id);
    },
    resetFilters() {
        this.filterStatus = '';
        this.filterType = '';
        this.filterCustomer = '';
        this.filterRegistrant = '';
        this.filterStartDate = '';
        this.filterEndDate = '';
        this.fetchComplaints(this.$route.params.id);
    },
    handleComplaintAdded() {
        this.showAddModal = false;
        this.fetchComplaints(this.$route.params.id);
    },
    viewDetails(complaint) {
      this.selectedComplaint = complaint;
      this.fetchComments(complaint.id);
    },
    async fetchComments(complaintId) {
      this.comments = [];
      try {
        const response = await api.get('comments/', { params: { complaint: complaintId } });
        this.comments = response.data;
      } catch (error) {
        console.error("Failed to fetch comments", error);
      }
    },
    handleCommentImageChange(event) {
        const file = event.target.files[0];
        if (file) {
            if (file.size > 10 * 1024 * 1024) { // 10MB limit
                alert('图片大小不能超过10MB');
                event.target.value = '';
                this.newCommentImage = null;
                return;
            }
            this.newCommentImage = file;
        }
    },
    async submitComment() {
      if (!this.newComment.trim() && !this.newCommentImage) return;
      this.submittingComment = true;
      try {
        const formData = new FormData();
        formData.append('complaint', this.selectedComplaint.id);
        formData.append('content', this.newComment);
        if (this.newCommentImage) {
            formData.append('image', this.newCommentImage);
        }

        await api.post('comments/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        
        this.newComment = '';
        this.newCommentImage = null;
        // Reset file input
        const fileInput = document.querySelector('.comment-image-input');
        if (fileInput) fileInput.value = '';
        
        await this.fetchComments(this.selectedComplaint.id);
      } catch (error) {
        console.error("Failed to submit comment", error);
        alert("提交备注失败");
      } finally {
        this.submittingComment = false;
      }
    },
    truncate(text, length) {
      if (!text) return '';
      return text.length > length ? text.substring(0, length) + '...' : text;
    },
    formatStatus(status) {
      const map = {
        'pending': '待处理',
        'in_progress': '处理中',
        'resolved': '已解决'
      };
      return map[status] || status;
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    canEditComplaint(complaint) {
        return complaint && complaint.can_edit;
    },
    editComplaint(complaint) {
        // Open the ComplaintForm modal in edit mode
        // Since we are reusing ComplaintForm which handles 'isEdit' via props or we can just pass data
        // But wait, ProjectComplaints uses ComplaintForm for CREATION.
        // We need to trigger the edit mode.
        // Let's check how ComplaintForm is used.
        this.selectedComplaint = null; // Close detail view
        this.editingComplaint = complaint; // Set complaint to edit
        this.showForm = true; // Show form
    },
    handleFormSuccess() {
        this.showForm = false;
        this.editingComplaint = null;
        this.fetchComplaints();
    },
    handleFormCancel() {
        this.showForm = false;
        this.editingComplaint = null;
    },
    async updateStatus(complaint, newStatus) {
      if (!confirm(`确定将状态更新为"${this.formatStatus(newStatus)}"?`)) return;
      try {
        await api.patch(`complaints/${complaint.id}/`, { status: newStatus });
        
        // Update local state
        complaint.status = newStatus;
        
        // Update list
        const index = this.complaints.findIndex(c => c.id === complaint.id);
        if (index !== -1) {
            this.complaints[index].status = newStatus;
        }
        // alert('状态更新成功');
      } catch (err) {
        alert('状态更新失败: ' + (err.response?.data?.detail || err.message));
      }
    }
  }
};
</script>

<style scoped>
.project-complaints-page {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-header h2 {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.025em;
}

.project-code {
  background-color: #EEF2FF;
  color: #4F46E5;
  padding: 6px 10px;
  border-radius: 6px;
  font-family: 'Monaco', 'Consolas', monospace;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
}

/* Filters & Control Panel */
.filter-panel {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  margin-bottom: 24px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f1f5f9;
  background: #fff;
}

.filter-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-icon-box {
  width: 32px;
  height: 32px;
  background: #EEF2FF;
  color: #4f46e5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filter-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.filter-actions {
  display: flex;
  gap: 12px;
}

.filter-content {
  padding: 20px 24px;
  background: #f8fafc;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 160px;
}

.filter-group.wide {
  min-width: 280px;
  flex: 1.5;
}

.filter-group label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
}

.modern-select, .modern-input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background-color: white;
  color: #334155;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.modern-select:focus, .modern-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
  outline: none;
}

.input-with-icon {
  position: relative;
}

.input-with-icon .modern-input {
  padding-left: 36px;
}

.field-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
}

.date-range-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 4px;
}

.date-range-wrapper:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.date-input {
  border: none;
  background: transparent;
  height: 32px;
  font-size: 0.85rem;
  padding: 0 8px;
  color: #334155;
  width: 130px;
}

.date-input:focus {
  box-shadow: none;
}

.range-separator {
  color: #94a3b8;
  font-size: 0.8rem;
}

.btn-light {
  background: white;
  border: 1px solid #e2e8f0;
  color: #64748b;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  gap: 8px;
}

.btn-light:hover {
  background: #f1f5f9;
  color: #4f46e5;
  border-color: #cbd5e1;
}

.btn-icon {
  background: white;
  border: 1px solid #e2e8f0;
  color: #64748b;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  color: #4f46e5;
  border-color: #4f46e5;
  background-color: #EEF2FF;
}

/* Skeleton Loader */
.skeleton-loader {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.skeleton-header {
  height: 40px;
  background: #f1f5f9;
  border-radius: 6px;
  margin-bottom: 20px;
}

.skeleton-row {
  height: 60px;
  background: #f8fafc;
  margin-bottom: 12px;
  border-radius: 6px;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Table Enhancements */
.complaints-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  overflow-x: auto;
  border: 1px solid #e2e8f0;
}

.complaints-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 1000px; /* Prevent squishing on small screens */
}

.complaints-table th, .complaints-table td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.complaints-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #475569;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
  position: sticky;
  top: 0;
  z-index: 10;
}

.complaints-table tbody tr {
  transition: background-color 0.2s ease;
}

.complaints-table tbody tr:hover {
  background-color: #f8fafc;
}

.complaints-table tbody tr:last-child td {
  border-bottom: none;
}

/* Column Specific Styles - No Compression */
.complaints-table th:nth-child(1), .complaints-table td:nth-child(1) { 
    min-width: 140px; 
    white-space: nowrap;
}

/* Restored Enhancements */
h2 {
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #0f172a;
}

.modal-overlay {
  backdrop-filter: blur(8px); /* Stronger blur for glassmorphism */
}

.modal-content {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); /* Deeper shadow */
  border: 1px solid rgba(255, 255, 255, 0.1);
} /* Code */

.complaints-table th:nth-child(2), .complaints-table td:nth-child(2) { 
    min-width: 200px; 
} /* Title */

.complaints-table th:nth-child(3), .complaints-table td:nth-child(3) { 
    min-width: 150px; 
} /* Customer */

.complaints-table th:nth-child(4), .complaints-table td:nth-child(4) { 
    min-width: 120px; 
} /* Type */

.complaints-table th:nth-child(5), .complaints-table td:nth-child(5) { 
    min-width: 120px; 
} /* Registrant */

.complaints-table th:nth-child(6), .complaints-table td:nth-child(6) { 
    min-width: 120px; 
} /* Status */

.complaints-table th:nth-child(7), .complaints-table td:nth-child(7) { 
    min-width: 180px; 
    white-space: nowrap;
} /* Date */

.complaints-table th:nth-child(8), .complaints-table td:nth-child(8) { 
    min-width: 100px; 
    text-align: right;
    white-space: nowrap;
} /* Actions */
.complaints-table th:nth-child(8) {
    text-align: right;
}

/* Table Content Typography */
.complaints-table td {
    font-size: 0.95rem;
    color: #334155;
    line-height: 1.5;
}

.complaint-title {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
  /* Allow full title display */
  white-space: normal; 
}

.type-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background: #f1f5f9;
  color: #475569;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid #e2e8f0;
  white-space: nowrap;
}

/* Status Badge */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.status-badge::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 6px;
  background-color: currentColor;
}

.status-badge.pending { 
  background-color: #FFF7ED; 
  color: #C2410C; 
}
.status-badge.in_progress { 
  background-color: #EFF6FF; 
  color: #2563EB; 
}
.status-badge.resolved { 
  background-color: #ECFDF5; 
  color: #059669; 
}

/* Buttons */
.btn-text {
  background: none;
  border: none;
  color: #4f46e5;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.2s;
}

.btn-text:hover {
  background-color: #EEF2FF;
  text-decoration: none;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn-primary {
  background-color: #4f46e5;
  color: white;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.btn-primary:hover {
  background-color: #4338ca;
  box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: white;
  color: #1e293b;
  border-color: #cbd5e1;
}

.btn-secondary:hover {
  background-color: #f8fafc;
  border-color: #94a3b8;
}

.btn-refresh {
  height: 42px;
  padding: 0 20px;
  font-weight: 600;
  color: #475569;
  border-color: #cbd5e1;
  background-color: white;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-refresh:hover {
  background-color: #f8fafc;
  color: #4f46e5;
  border-color: #4f46e5;
}

.icon {
  margin-right: 0; /* Handled by gap */
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  border: 1px dashed #e2e8f0;
}

.empty-icon {
  color: #cbd5e1;
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

.empty-state p {
  color: #64748b;
  font-size: 1rem;
}

/* Loading & Error */
.loading-state, .error-state {
  text-align: center;
  padding: 60px;
  color: #64748b;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Modal Styles Refined */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  animation: fadeIn 0.2s ease-out;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-content.large-modal {
  max-width: 960px;
}

.modal-header {
  padding: 24px 32px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1e293b;
  font-weight: 600;
}

.close-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1.5rem;
}

.close-btn:hover {
  background-color: #f1f5f9;
  color: #ef4444;
}

.modal-body {
  padding: 32px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 24px 32px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  background-color: #f8fafc;
  border-radius: 0 0 16px 16px;
  gap: 12px;
}

.modal-footer.footer-spaced {
  justify-content: space-between;
}

.modal-footer.footer-spaced {
    justify-content: space-between;
}

.left-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* Detail View Styles */
.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item.full-width {
  grid-column: span 2;
}

.detail-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.label-icon {
  color: #94a3b8;
  width: 14px;
  height: 14px;
}

.detail-value {
  font-size: 1rem;
  color: #1e293b;
  font-weight: 500;
}

.title-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
}

/* Description Box */
.detail-group {
  margin-top: 24px;
}

.detail-text {
  margin-top: 12px;
  padding: 20px;
  background-color: #f8fafc;
  border-radius: 8px;
  color: #334155;
  line-height: 1.6;
  border: 1px solid #e2e8f0;
  font-size: 0.95rem;
}

/* Comments Section */
.comments-section {
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 20px;
  padding-bottom: 0;
  border: none;
}

.comments-container {
  background: transparent;
  border: none;
  padding: 0;
  margin-bottom: 24px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 8px;
}

.comments-list::-webkit-scrollbar {
  width: 6px;
}
.comments-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}
.comments-list::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 3px;
}

.comment-item {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
  margin-bottom: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.comment-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-user {
  font-weight: 600;
  font-size: 0.9rem;
  color: #4f46e5;
  background: #EEF2FF;
  padding: 4px 10px;
  border-radius: 999px;
}

.comment-time {
  font-size: 0.8rem;
  color: #94a3b8;
}

.comment-content {
  color: #334155;
  font-size: 0.95rem;
  line-height: 1.6;
}

.comment-image-container {
  margin-top: 12px;
}

.comment-image-preview {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.comment-image-preview:hover {
  transform: scale(1.02);
}

.add-comment {
  margin-top: 24px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.comment-tools {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 12px;
}

.comment-image-input {
  display: none;
}

.image-upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #64748b;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 500;
}

.image-upload-btn:hover {
  background: #f1f5f9;
  color: #4f46e5;
}

.file-name {
  font-size: 0.8rem;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #4f46e5;
}

/* Form Styles */
.form-group {
  margin-bottom: 20px;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #334155;
  font-size: 0.9rem;
}

.form-input, .form-select, .form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #1e293b;
  transition: all 0.2s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Audit Actions */
.audit-actions {
  display: flex;
  gap: 12px;
}

.btn-warning {
  background-color: #f59e0b;
  color: white;
}
.btn-warning:hover {
  background-color: #d97706;
}

.btn-success {
  background-color: #10b981;
  color: white;
}
.btn-success:hover {
  background-color: #059669;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.editor-tip {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-top: 6px;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 768px) {
  .grid-3 {
    grid-template-columns: 1fr;
  }
}

.text-danger {
  color: #ef4444;
}

.text-danger:hover {
  color: #dc2626;
  background-color: #FEF2F2;
}
</style>
