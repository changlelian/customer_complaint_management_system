<template>
  <div class="login-container">
    <div class="login-card">
      <h2>客诉问题管理系统</h2>
      <p class="subtitle">请输入您的账号</p>
      
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>用户名</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="Username" 
            required 
          />
        </div>
        
        <div class="input-group">
          <label>密码</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="Password" 
            required 
          />
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button type="submit" :disabled="loading" class="login-btn">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>
      
      <div class="footer-links">
        <router-link to="/">返回前台首页</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: null
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.post('login/', {
          username: this.username,
          password: this.password
        });
        
        const token = response.data.token;
        localStorage.setItem('auth_token', token);
        
        // Fetch user info to determine role
        const userResponse = await api.get('users/me/');
        const user = userResponse.data;
        
        // Determine role and redirect
        let role = 'ordinary';
        if (user.is_superuser) {
          role = 'admin';
        } else if (user.groups.some(g => g.name === '现场用户')) {
          role = 'field';
        } else if (user.groups.some(g => g.name === '审核用户')) {
          role = 'auditor';
        }
        
        localStorage.setItem('user_role', role);
        localStorage.setItem('user_info', JSON.stringify(user));

        if (role === 'admin' || role === 'auditor') {
          this.$router.push('/admin/projects');
        } else {
          this.$router.push('/');
        }
        
      } catch (err) {
        console.error(err);
        if (err.response && err.response.data) {
             const data = err.response.data;
             if (data.non_field_errors) {
                 this.error = data.non_field_errors[0];
             } else {
                 this.error = '登录失败，请检查用户名和密码';
             }
        } else {
            this.error = '登录失败，请检查用户名和密码';
        }
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h2 {
  margin-top: 0;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  margin-bottom: 30px;
  font-size: 0.9em;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

input:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.login-btn:hover {
  background-color: #5a6fd1;
}

.login-btn:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}

.error-message {
  color: #e53e3e;
  background-color: #fff5f5;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.footer-links {
  margin-top: 20px;
  font-size: 0.9rem;
}

.footer-links a {
  color: #667eea;
  text-decoration: none;
}

.footer-links a:hover {
  text-decoration: underline;
}
</style>
