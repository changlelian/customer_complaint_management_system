<template>
  <div class="complaint-list">
    <div class="header">
      <h2>投诉列表</h2>
    </div>

    <!-- Status Filter Tabs -->
    <div class="status-tabs" v-if="!loading && !error">
        <button 
            class="tab-btn" 
            :class="{ active: statusFilter === 'all' }"
            @click="statusFilter = 'all'">
            全部
            <span class="count-badge">{{ statusCounts.all }}</span>
        </button>
        <button 
            class="tab-btn" 
            :class="{ active: statusFilter === 'pending' }"
            @click="statusFilter = 'pending'">
            待处理
            <span class="count-badge pending">{{ statusCounts.pending }}</span>
        </button>
        <button 
            class="tab-btn" 
            :class="{ active: statusFilter === 'in_progress' }"
            @click="statusFilter = 'in_progress'">
            处理中
            <span class="count-badge in_progress">{{ statusCounts.in_progress }}</span>
        </button>
        <button 
            class="tab-btn" 
            :class="{ active: statusFilter === 'resolved' }"
            @click="statusFilter = 'resolved'">
            已解决
            <span class="count-badge resolved">{{ statusCounts.resolved }}</span>
        </button>
    </div>
    
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      {{ error }}
    </div>
    
    <div v-else>
      <div v-if="filteredComplaints.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        <p>暂无相关投诉记录</p>
      </div>
      
      <div v-else class="cards">
        <div v-for="complaint in filteredComplaints" :key="complaint.id" class="card" @click="viewDetails(complaint)">
          <div class="card-header">
            <div class="header-top">
                <span class="code-badge" v-if="complaint.complaint_code">{{ complaint.complaint_code }}</span>
                <span :class="['status-badge', complaint.status]">
                {{ formatStatus(complaint.status) }}
                </span>
            </div>
            <h3 class="card-title">{{ complaint.title }}</h3>
          </div>
          
          <div class="card-body">
            <div class="info-grid">
              <div class="info-item">
                <span class="label">客户:</span>
                <span class="value">{{ complaint.customer_name }}</span>
              </div>
              <div class="info-item">
                <span class="label">项目:</span>
                <span class="value">{{ complaint.project_name || '未知项目' }}</span>
              </div>
              <div class="info-item">
                <span class="label">类型:</span>
                <span class="value">{{ complaint.type_name || '未分类' }}</span>
              </div>
              <div class="info-item">
                <span class="label">登记人:</span>
                <span class="value">{{ complaint.registrant_name || '未知' }}</span>
              </div>
            </div>
            
            <div class="description-preview">
              {{ stripHtml(complaint.description) }}
            </div>
          </div>
          
          <div class="card-footer">
            <span class="date">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              {{ formatDate(complaint.created_at) }}
            </span>
            <div class="card-actions">
                <button v-if="canEdit(complaint)" class="btn-text" @click.stop="startEdit(complaint)" style="margin-right: 8px;">编辑</button>
                <button class="btn-text" @click.stop="viewDetails(complaint)">查看详情</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- View Details Modal -->
    <div v-if="selectedComplaint" class="modal-overlay" @click.self="selectedComplaint = null">
      <div class="modal-content large-modal">
        <div class="modal-header">
          <h3>问题详情</h3>
          <button class="close-btn" @click="selectedComplaint = null">&times;</button>
        </div>
        <div class="modal-body detail-view">
          <div class="detail-header">
             <div class="title-group">
                 <span class="detail-code" v-if="selectedComplaint.complaint_code">{{ selectedComplaint.complaint_code }}</span>
                 <h4>{{ selectedComplaint.title }}</h4>
             </div>
             <div class="header-actions">
                 <button v-if="canEdit(selectedComplaint)" @click="startEdit(selectedComplaint)" class="btn btn-outline-primary btn-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    编辑
                 </button>
                 <span :class="['status-badge', selectedComplaint.status]">
                  {{ formatStatus(selectedComplaint.status) }}
                </span>
             </div>
          </div>

          <div class="detail-grid">
             <div class="detail-item">
               <span class="detail-label">
                 <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="label-icon"><path d="M3 21h18"/><path d="M5 21V7l8-4 8 4v14"/><path d="M17 21v-8H7v8"/></svg>
                 项目
               </span>
               <span class="detail-value">{{ selectedComplaint.project_name }}</span>
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

          <div class="detail-section">
            <div class="section-title">详细描述</div>
            <div class="detail-content ql-snow">
              <div class="ql-editor" v-html="selectedComplaint.description"></div>
            </div>
          </div>
          
          <div class="detail-section" v-if="selectedComplaint.attachment">
            <span class="detail-label block">附件:</span>
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
        <div class="modal-footer">
           <button class="btn btn-primary" @click="selectedComplaint = null">关闭</button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal-content">
        <div class="modal-header">
             <!-- Header handled by form component or hidden -->
             <button class="close-btn" @click="showEditModal = false">&times;</button>
        </div>
        <div class="modal-body">
            <ComplaintForm 
                :initialData="editingComplaint" 
                @submit-success="onComplaintUpdated" 
            />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';
import '@vueup/vue-quill/dist/vue-quill.snow.css';
import ComplaintForm from './ComplaintForm.vue';

export default {
  name: 'ComplaintList',
  components: { ComplaintForm },
  props: {
    projectId: {
      type: [Number, String],
      default: null
    }
  },
  data() {
    return {
      complaints: [],
      loading: true,
      error: null,
      selectedComplaint: null,
      statusFilter: 'all',
      showEditModal: false,
      editingComplaint: null,
      currentUser: null,
      userRole: null,
      comments: [],
      newComment: '',
      newCommentImage: null,
      submittingComment: false
    };
  },
  computed: {
    filteredComplaints() {
        if (this.statusFilter === 'all') {
            return this.complaints;
        }
        return this.complaints.filter(c => c.status === this.statusFilter);
    },
    statusCounts() {
        const counts = {
            all: this.complaints.length,
            pending: 0,
            in_progress: 0,
            resolved: 0
        };
        this.complaints.forEach(c => {
            if (counts[c.status] !== undefined) {
                counts[c.status]++;
            }
        });
        return counts;
    }
  },
  watch: {
    projectId() {
      this.fetchComplaints();
    }
  },
  created() {
    this.fetchComplaints();
    this.loadUserInfo();
  },
  methods: {
    loadUserInfo() {
        this.currentUser = localStorage.getItem('username');
        this.userRole = localStorage.getItem('role'); // 'field', 'admin', 'auditor', 'ordinary'
    },
    async fetchComplaints() {
      // Don't fetch if no auth token (though Home.vue handles this now)
      if (!localStorage.getItem('auth_token')) {
        this.loading = false;
        return;
      }
      try {
        this.loading = true;
        const params = {};
        if (this.projectId) {
            params.project = this.projectId;
        }
        const response = await api.get('complaints/', { params });
        this.complaints = response.data;
        this.error = null;
      } catch (err) {
        if (err.response && err.response.status === 401) {
            // Token invalid or expired
            this.error = '登录已过期，请重新登录';
        } else {
            this.error = '无法加载投诉列表';
        }
        console.error(err);
      } finally {
        this.loading = false;
      }
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
    stripHtml(html) {
        if (!html) return '';
        // Create a temporary element to strip HTML
        const tmp = document.createElement("DIV");
        tmp.innerHTML = html;
        let text = tmp.textContent || tmp.innerText || "";
        // Truncate if too long
        if (text.length > 100) {
            text = text.substring(0, 100) + '...';
        }
        return text;
    },
    viewDetails(complaint) {
        this.selectedComplaint = complaint;
        this.fetchComments(complaint.id);
    },
    canEdit(complaint) {
        // Use the backend-provided permission flag if available
        if (complaint.can_edit !== undefined) {
            return complaint.can_edit;
        }
        
        // Fallback logic (should rarely be reached if backend is updated)
        if (!this.currentUser || !this.userRole) return false;
        
        if (this.userRole === 'field') {
            // Field users can edit their own complaints
            return complaint.registrant_name === this.currentUser;
        }
        if (this.userRole === 'admin' || this.userRole === 'auditor') return true;
        
        return false;
    },
    startEdit(complaint) {
        this.editingComplaint = complaint;
        this.selectedComplaint = null; // Close detail
        this.showEditModal = true;
    },
    onComplaintUpdated() {
        this.showEditModal = false;
        this.editingComplaint = null;
        this.fetchComplaints(); // Refresh list
    },
    async fetchComments(complaintId) {
        this.comments = [];
        try {
            // Using the nested action we created: GET /complaints/{id}/comments/
            // Or the ViewSet: GET /comments/?complaint={id}
            // Let's use the ViewSet approach as it's cleaner for filtering usually, 
            // but the nested action is also fine. I implemented both? 
            // I implemented comments action in ComplaintViewSet AND CommentViewSet.
            // Let's use CommentViewSet: api.get('comments/', { params: { complaint: complaintId } })
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
    }
  }
};
</script>

<style scoped>
.complaint-list {
  /* Remove container background to let cards float on dashboard bg */
  padding: 0; 
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

/* Tabs */
.status-tabs {
    display: flex;
    gap: 12px;
    margin-bottom: 32px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 16px;
    overflow-x: auto;
}

.tab-btn {
    background: transparent;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 500;
    border: 1px solid transparent;
}

.tab-btn:hover {
    background-color: var(--bg-surface);
    color: var(--text-main);
    box-shadow: var(--shadow-sm);
}

.tab-btn.active {
    background-color: var(--text-main);
    color: white;
    box-shadow: var(--shadow-md);
}

.count-badge {
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 999px;
    background-color: rgba(0,0,0,0.05);
    color: var(--text-secondary);
    min-width: 20px;
    text-align: center;
    font-weight: 600;
}

.tab-btn.active .count-badge {
    background-color: rgba(255,255,255,0.2);
    color: white;
}

/* Specific badge colors only when not active if desired, 
   but unified dark theme for active tab looks cleaner. 
   Let's keep colored badges for non-active states. */
.tab-btn:not(.active) .count-badge.pending { background-color: var(--warning-bg); color: var(--warning-text); }
.tab-btn:not(.active) .count-badge.in_progress { background-color: var(--info-bg); color: var(--info-text); }
.tab-btn:not(.active) .count-badge.resolved { background-color: var(--success-bg); color: var(--success-text); }


.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 60px 0;
  color: var(--text-muted);
}

.empty-icon {
  color: var(--text-light);
  margin-bottom: 16px;
  opacity: 0.5;
}

.spinner {
  border: 3px solid rgba(0, 0, 0, 0.1);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border-left-color: var(--primary-color);
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  background-color: white;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
  border-color: var(--primary-light);
}

.card-header {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 8px;
  background-color: white;
}

.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.code-badge {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--primary-color);
    background-color: var(--primary-bg);
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.05em;
}

.card-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.status-badge {
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 999px;
  font-weight: 600;
  text-transform: uppercase;
  white-space: nowrap;
  letter-spacing: 0.05em;
}

.status-badge.pending { background-color: var(--warning-bg); color: var(--warning-text); }
.status-badge.in_progress { background-color: var(--info-bg); color: var(--info-text); }
.status-badge.resolved { background-color: var(--success-bg); color: var(--success-text); }

.card-body {
  padding: 12px 16px;
  flex: 1;
}

.info-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 8px;
    margin-bottom: 12px;
}

.info-item {
  font-size: 0.85rem;
  display: flex;
  flex-direction: column;
  min-width: 0; /* Critical for truncation in grid */
}

.label {
  color: var(--text-muted);
  font-size: 0.7rem;
  margin-bottom: 2px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.value {
  color: var(--text-secondary);
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.description-preview {
  margin-top: 12px;
  color: var(--text-secondary);
  font-size: 0.85rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  background: var(--bg-body);
  padding: 10px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
}

.card:hover .description-preview {
    border-color: var(--border-color);
    background: white;
}

.card-footer {
  padding: 12px 16px;
  background-color: var(--bg-body);
  border-top: 1px solid var(--border-color);
  font-size: 0.8rem;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.card-actions {
    display: flex;
    align-items: center;
}

.btn-text {
    background: none;
    border: none;
    color: var(--primary-color);
    font-weight: 600;
    cursor: pointer;
    padding: 0;
    font-size: 0.85rem;
    transition: color 0.2s;
}

.btn-text:hover {
    color: var(--primary-hover);
    text-decoration: underline;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
  animation: fadeIn 0.2s;
}

.modal-content {
  background: white;
  border-radius: var(--radius-lg);
  width: 90%;
  max-width: 750px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-lg);
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-header {
  padding: 20px 32px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-body);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  flex-shrink: 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--text-main);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-muted);
  transition: color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.close-btn:hover {
    background-color: rgba(0,0,0,0.05);
    color: var(--text-main);
}

.modal-body {
  padding: 32px;
  overflow-y: auto;
  flex: 1;
}



.modal-footer {
  padding: 20px 32px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  background-color: var(--bg-body);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
  gap: 12px;
  flex-shrink: 0;
}

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
}

.title-group {
    flex: 1;
    padding-right: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.detail-code {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--primary-color);
    background-color: var(--primary-bg);
    padding: 2px 8px;
    border-radius: 4px;
    align-self: flex-start;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
}

.detail-header h4 {
    margin: 0;
    font-size: 1.5rem;
    color: var(--text-main);
    line-height: 1.3;
}

.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 24px;
    margin-bottom: 32px;
    background: var(--bg-body);
    padding: 20px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
}

.detail-item {
    display: flex;
    flex-direction: column;
}

.detail-label {
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    display: flex;
    align-items: center;
}

.label-icon {
    margin-right: 6px;
    color: var(--primary-color);
    opacity: 0.8;
}

.detail-label.block {
    display: block;
    margin-bottom: 12px;
}

.detail-value {
    font-size: 0.95rem;
    color: var(--text-main);
    font-weight: 500;
}

.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 16px;
    padding-left: 12px;
    border-left: 3px solid var(--primary-color);
}

.comments-section {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid var(--border-color);
}

.comments-container {
    background: var(--bg-body);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px;
    margin-bottom: 20px;
}

.comments-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    max-height: 400px;
    overflow-y: auto;
    padding-right: 8px;
}

/* Custom Scrollbar for Comments */
.comments-list::-webkit-scrollbar {
    width: 6px;
}
.comments-list::-webkit-scrollbar-track {
    background: transparent;
}
.comments-list::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
}
.comments-list::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0, 0, 0, 0.2);
}

.comment-item {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    transition: all 0.2s;
}

.comment-item:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border-color: var(--primary-light);
}

.comment-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 0.85rem;
    border-bottom: none;
    padding-bottom: 0;
}

.comment-user {
    font-weight: 600;
    color: var(--text-main);
    background: #EEF2FF;
    color: var(--primary-color);
    padding: 2px 8px;
    border-radius: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.comment-time {
    color: var(--text-muted);
}

.comment-content {
    color: var(--text-main);
    font-size: 0.95rem;
    line-height: 1.6;
    white-space: pre-wrap;
}

.comment-image-container {
    margin-top: 12px;
}

.comment-image-preview {
    max-width: 200px;
    max-height: 200px;
    border-radius: 4px;
    border: 1px solid var(--border-color);
    cursor: zoom-in;
    transition: transform 0.2s;
}

.comment-image-preview:hover {
    transform: scale(1.02);
}

.no-comments {
    color: var(--text-muted);
    text-align: center;
    padding: 32px 0;
    font-style: italic;
}

.add-comment {
    background: var(--bg-body);
    padding: 16px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
}

.comment-tools {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
}

.comment-image-input {
    display: none;
}

.image-upload-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 6px 12px;
    border-radius: 4px;
    transition: background 0.2s;
}

.image-upload-btn:hover {
    background: rgba(0,0,0,0.05);
    color: var(--primary-color);
}

.file-name {
    font-size: 0.8rem;
    color: var(--primary-color);
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.form-textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    resize: vertical;
    font-family: inherit;
    font-size: 0.9rem;
    transition: border-color 0.2s;
    background: white;
}

.form-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 2px var(--primary-light);
}

.detail-content {
    background: white;
    padding: 24px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    min-height: 100px;
}

.detail-section {
    margin-bottom: 32px;
}

.modal-footer {
  padding: 20px 32px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  background-color: var(--bg-body);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.btn-outline-primary {
    border: 1px solid var(--primary-color);
    color: var(--primary-color);
    background: transparent;
    padding: 6px 12px;
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
}

.btn-outline-primary:hover {
    background: var(--primary-bg);
}
</style>
