<template>
  <router-view></router-view>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
/* Global Reset & Base Styles */
:root {
  --primary-color: #4F46E5; /* Indigo 600 */
  --primary-hover: #4338CA; /* Indigo 700 */
  --secondary-color: #64748B; /* Slate 500 */
  --success-color: #10B981; /* Emerald 500 */
  --danger-color: #EF4444; /* Red 500 */
  --danger-hover: #DC2626; /* Red 600 */
  --background-color: #F3F4F6; /* Gray 100 */
  --surface-color: #FFFFFF;
  --text-main: #1F2937; /* Gray 800 */
  --text-muted: #6B7280; /* Gray 500 */
  --border-color: #E5E7EB; /* Gray 200 */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --radius: 8px;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--background-color);
  color: var(--text-main);
  line-height: 1.5;
}

h1, h2, h3, h4, h5, h6 {
  margin: 0;
  font-weight: 600;
  color: var(--text-main);
}

button {
  font-family: inherit;
}

/* Common Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  border: 1px solid transparent;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}
.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
}

.btn-danger {
  background-color: var(--danger-color);
  color: white;
}
.btn-danger:hover:not(:disabled) {
  background-color: var(--danger-hover);
}

.btn-secondary {
  background-color: white;
  border-color: var(--border-color);
  color: var(--text-main);
}
.btn-secondary:hover:not(:disabled) {
  background-color: #F9FAFB;
  border-color: #D1D5DB;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Common Input Styles */
input, select, textarea {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--text-main);
  background-color: var(--surface-color);
  background-clip: padding-box;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--primary-color);
  outline: 0;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

/* Table Styles */
.table-container {
  background: var(--surface-color);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #F9FAFB;
  color: var(--text-muted);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  padding: 0.75rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-main);
  font-size: 0.875rem;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background-color: #F9FAFB;
}

/* Transition for router view */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
