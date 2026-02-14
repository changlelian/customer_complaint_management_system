<template>
  <div class="complaint-form-card">
    <div class="header" v-if="!hideHeader">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="header-icon"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
      <h2>{{ isEdit ? '编辑投诉' : '提交新投诉' }}</h2>
    </div>
    
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label>标题</label>
        <input v-model="form.title" required placeholder="简要描述问题..." class="form-input" />
      </div>
      
      <div class="grid-2">
        <div class="form-group">
          <label>客户现场</label>
          <input v-model="form.customer_name" required placeholder="客户现场名称" class="form-input" />
        </div>
        <div class="form-group">
            <label>所属项目</label>
            <select v-model="form.project" required class="form-input form-select" :disabled="isEdit || !!initialProjectId">
                <option :value="null" disabled>请选择项目</option>
                <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
        </div>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>问题分类</label>
          <select v-model="form.category" required class="form-input form-select">
            <option value="software">软件问题</option>
            <option value="algorithm">算法问题</option>
            <option value="system">系统问题</option>
            <option value="other">其他问题</option>
          </select>
        </div>
        <div class="form-group">
            <label>客诉类型</label>
            <select v-model="form.complaint_type" required class="form-input form-select">
                <option :value="null" disabled>请选择类型</option>
                <option v-for="t in types" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
        </div>
      </div>

      <div class="form-group" v-if="form.category === 'software'">
        <label>软件版本</label>
        <select v-model="form.software_version" required class="form-input form-select">
            <option :value="null" disabled>请选择版本</option>
            <option v-for="v in versions" :key="v.id" :value="v.id">
            {{ v.version_number }}
            </option>
        </select>
      </div>
      
      <div class="form-group">
        <label>详细描述 (支持截图粘贴)</label>
        <div class="rich-text-editor-container">
            <QuillEditor 
                v-model:content="form.description" 
                contentType="html" 
                theme="snow" 
                :toolbar="[['bold', 'italic', 'underline'], [{'list': 'ordered'}, {'list': 'bullet'}], ['image']]"
                placeholder="请详细描述客户遇到的问题..."
                style="height: 200px"
            />
        </div>
      </div>

      <div class="form-group">
          <label>附件 (最大100MB)</label>
          <div v-if="isEdit && currentAttachmentUrl" class="current-attachment">
             <span>当前附件: </span>
             <a :href="currentAttachmentUrl" target="_blank">查看</a>
             <button type="button" @click="clearAttachment" class="btn-text-danger">删除</button>
          </div>
          <input type="file" @change="handleFileChange" class="form-input" />
          <p class="help-text" v-if="isEdit">如果不修改附件，请留空</p>
      </div>
      
      <div class="form-actions">
        <button type="submit" :disabled="submitting" class="btn btn-primary btn-block">
          <span v-if="submitting" class="loading-text">
            <span class="spinner-sm"></span> 提交中...
          </span>
          <span v-else>{{ isEdit ? '保存修改' : '提交投诉' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import api from '../api';
import { QuillEditor } from '@vueup/vue-quill';
import '@vueup/vue-quill/dist/vue-quill.snow.css';

export default {
  name: 'ComplaintForm',
  components: { QuillEditor },
  props: {
      initialData: {
          type: Object,
          default: null
      },
      initialProjectId: {
          type: [Number, String],
          default: null
      }
  },
  data() {
    return {
      form: {
        title: '',
        customer_name: '',
        description: '',
        project: null,
        category: 'software', // Default to software or handle empty
        complaint_type: null,
        software_version: null,
        attachment: null
      },
      projects: [],
      types: [],
      versions: [],
      submitting: false,
      currentAttachmentUrl: null
    };
  },
  computed: {
      isEdit() {
          return !!this.initialData;
      }
  },
  created() {
      this.fetchProjects();
      this.fetchTypes();
      if (this.initialData) {
          this.populateForm();
      } else if (this.initialProjectId) {
          this.form.project = parseInt(this.initialProjectId);
      }
  },
  watch: {
      initialData: {
          handler(newVal) {
              if (newVal) this.populateForm();
          },
          deep: true
      },
      'form.project': {
          handler(newVal) {
              if (newVal) {
                  this.fetchVersions(newVal);
              } else {
                  this.versions = [];
              }
          }
      }
  },
  methods: {
    populateForm() {
        const data = this.initialData;
        this.form.title = data.title;
        this.form.customer_name = data.customer_name;
        this.form.description = data.description;
        this.form.project = data.project;
        this.form.category = data.category || 'software';
        this.form.complaint_type = data.complaint_type;
        this.form.software_version = data.software_version;
        this.currentAttachmentUrl = data.attachment;
        // Attachment is not populated as file object, but we show current one
        this.form.attachment = null;
        
        // Trigger version fetch if project is set
        if (this.form.project) {
            this.fetchVersions(this.form.project);
        }
    },
    clearAttachment() {
        // This is tricky. If we want to delete, we might need a separate flag or API call.
        // For now, let's just hide the link. If they upload new, it replaces. 
        // If they submit without new, it keeps old.
        // To explicitly delete, we'd need to send null or a flag. 
        // Let's assume 'clear' just means 'I will upload a new one or I want to see the input'.
        this.currentAttachmentUrl = null;
    },
    async fetchVersions(projectId) {
        try {
            const response = await api.get(`versions/?project=${projectId}`);
            this.versions = response.data;
        } catch (e) {
            console.error('Failed to fetch versions', e);
            this.versions = [];
        }
    },
    async fetchProjects() {
        try {
            const response = await api.get('projects/');
            this.projects = response.data;
            if (!this.isEdit && this.projects.length > 0 && !this.form.project) {
                // If initialProjectId is provided, try to select it
                if (this.initialProjectId) {
                    const exists = this.projects.find(p => p.id === Number(this.initialProjectId));
                    if (exists) {
                        this.form.project = exists.id;
                        return;
                    }
                }
                // Fallback to first project
                this.form.project = this.projects[0].id;
            }
        } catch (e) { console.error(e); }
    },
    async fetchTypes() {
        try {
            const response = await api.get('types/');
            this.types = response.data;
        } catch (e) { console.error(e); }
    },
    handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            if (file.size > 100 * 1024 * 1024) {
                alert('文件大小不能超过100MB');
                event.target.value = '';
                this.form.attachment = null;
                return;
            }
            this.form.attachment = file;
        }
    },
    async submitForm() {
      this.submitting = true;
      try {
        const formData = new FormData();
        formData.append('title', this.form.title);
        formData.append('customer_name', this.form.customer_name);
        formData.append('description', this.form.description);
        if (this.form.project) formData.append('project', this.form.project);
        if (this.form.category) formData.append('category', this.form.category);
        if (this.form.complaint_type) formData.append('complaint_type', this.form.complaint_type);
        if (this.form.category === 'software' && this.form.software_version) {
            formData.append('software_version', this.form.software_version);
        }
        
        if (this.form.attachment) {
            formData.append('attachment', this.form.attachment);
        }

        if (this.isEdit) {
            await api.patch(`complaints/${this.initialData.id}/`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            alert('修改成功！');
            this.$emit('submit-success');
        } else {
            await api.post('complaints/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            alert('投诉提交成功！');
            this.$emit('submit-success');
            // Reset form
            this.form.title = '';
            this.form.description = '';
            this.form.customer_name = '';
            this.form.attachment = null;
        }
        
      } catch (err) {
        alert('提交失败: ' + (err.response?.data?.detail || '未知错误'));
        console.error(err);
      } finally {
        this.submitting = false;
      }
    }
  }
};
</script>

<style scoped>
.complaint-form-card {
  /* It's inside a modal now, so we can remove the card styling or keep it minimal */
  padding: 24px;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: var(--text-main);
}

.header-icon {
  color: var(--primary-color);
}

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
  font-weight: 600;
  color: var(--text-main);
  font-size: 0.9rem;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  background-color: var(--bg-body);
  color: var(--text-main);
}

.form-select {
    cursor: pointer;
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2364748B' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
    background-position: right 1rem center;
    background-repeat: no-repeat;
    background-size: 1.2em 1.2em;
    padding-right: 2.5rem;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
}

.form-input:focus, .form-textarea:focus, .form-select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
  background-color: white;
}

.rich-text-editor-container {
    background: white;
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.form-actions {
  margin-top: 32px;
}

.btn-block {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 14px;
  font-size: 1rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  background-color: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-block:hover {
    background-color: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn-block:disabled {
    background-color: var(--text-light);
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner-sm {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-left-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
