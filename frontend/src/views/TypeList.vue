<template>
  <div class="management-page">
    <div class="page-header">
      <h2>客诉类型列表</h2>
      <button @click="showAddModal = true" class="btn btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
        添加类型
      </button>
    </div>

    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>名称</th>
            <th class="text-right">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="type in types" :key="type.id">
            <td>
              <input v-if="editingId === type.id" v-model="editingType.name" class="form-input" />
              <span v-else class="type-name">{{ type.name }}</span>
            </td>
            <td class="text-right">
              <template v-if="editingId === type.id">
                <div class="action-group">
                  <button @click="saveEdit(type.id)" class="btn btn-primary btn-sm">保存</button>
                  <button @click="cancelEdit" class="btn btn-secondary btn-sm">取消</button>
                </div>
              </template>
              <template v-else>
                <div class="action-group">
                  <button @click="startEdit(type)" class="btn btn-secondary btn-sm">编辑</button>
                  <button @click="deleteType(type.id)" class="btn btn-danger btn-sm">删除</button>
                </div>
              </template>
            </td>
          </tr>
          <tr v-if="types.length === 0">
            <td colspan="2" class="empty-state">
              暂无客诉类型数据
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Type Modal -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3>添加新类型</h3>
          <button @click="showAddModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>类型名称</label>
            <input v-model="newType.name" placeholder="请输入客诉类型名称" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAddModal = false" class="btn btn-secondary">取消</button>
          <button @click="createType" :disabled="!newType.name" class="btn btn-primary">确认添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      types: [],
      newType: { name: '' },
      editingId: null,
      editingType: { name: '' },
      showAddModal: false
    };
  },
  created() {
    this.fetchTypes();
  },
  methods: {
    async fetchTypes() {
      try {
        const response = await api.get('types/');
        this.types = response.data;
      } catch (err) {
        console.error('加载类型失败', err);
        // alert('加载类型失败');
      }
    },
    async createType() {
      try {
        await api.post('types/', this.newType);
        this.newType = { name: '' };
        this.showAddModal = false;
        this.fetchTypes();
      } catch (err) {
        console.error('创建失败', err);
        alert('创建失败: ' + (err.response?.data?.detail || '未知错误'));
      }
    },
    startEdit(type) {
      this.editingId = type.id;
      this.editingType = { ...type };
    },
    cancelEdit() {
      this.editingId = null;
      this.editingType = { name: '' };
    },
    async saveEdit(id) {
      try {
        await api.put(`types/${id}/`, this.editingType);
        this.editingId = null;
        this.fetchTypes();
      } catch (err) {
        console.error('更新失败', err);
        alert('更新失败: ' + (err.response?.data?.detail || '未知错误'));
      }
    },
    async deleteType(id) {
      if (!confirm('确定删除?')) return;
      try {
        await api.delete(`types/${id}/`);
        this.fetchTypes();
      } catch (err) {
        console.error('删除失败', err);
        alert('删除失败: ' + (err.response?.data?.detail || '未知错误'));
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
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.icon {
  margin-right: 8px;
}

/* Table Styles */
.table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.data-table th, .data-table td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.data-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #475569;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.data-table tbody tr {
  transition: background-color 0.2s ease;
}

.data-table tbody tr:hover {
  background-color: #f8fafc;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.type-name {
  font-weight: 500;
  color: #334155;
  font-size: 0.95rem;
}

.text-right {
  text-align: right;
}

.action-group {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
  border-radius: 6px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: modal-slide-in 0.3s ease-out;
}

@keyframes modal-slide-in {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #94a3b8;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #64748b;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #334155;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #1e293b;
  transition: all 0.2s;
}

input:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background-color: #f8fafc;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}
</style>
