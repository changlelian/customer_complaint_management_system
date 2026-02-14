import { createRouter, createWebHistory } from 'vue-router';
import AdminLayout from '../components/AdminLayout.vue';
import ProjectList from '../views/ProjectList.vue';
import TypeList from '../views/TypeList.vue';
import UserList from '../views/UserList.vue';
import VersionList from '../views/VersionList.vue';
import ProjectComplaints from '../views/ProjectComplaints.vue';
import Login from '../views/Login.vue';
import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      { path: 'projects', component: ProjectList },
      { path: 'types', component: TypeList },
      { path: 'versions', component: VersionList },
      { path: 'users', component: UserList },
      { path: 'complaints/project/:id', component: ProjectComplaints },
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('auth_token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
