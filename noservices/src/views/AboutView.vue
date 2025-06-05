<template>
  <div class="about">
    <h1>About This Dashboard</h1>
    <p>
      This dashboard is an interactive management tool for inventory, sales, and orders. It
      integrates with multiple microservices:
    </p>
    <ul>
      <li><b>Inventory Service</b>: Manage and track stock items.</li>
      <li><b>Order Service</b>: View and process orders.</li>
      <li><b>Analytics Service</b>: See sales and inventory statistics.</li>
      <li><b>Media Service</b>: Upload and manage product images.</li>
      <li><b>Notification Service</b>: Send notifications to users.</li>
      <li><b>Audit Service</b>: Track user actions and changes.</li>
      <li><b>Search Service</b>: Search inventory and orders.</li>
      <li><b>Auth Service</b>: Secure login with Google OAuth2.</li>
    </ul>
    <p>
      Use the navigation menu to access each feature. All data is fetched live from the backend
      microservices.
    </p>
  </div>
</template>

<style scoped>
.about {
  min-height: 100vh;
  display: flex;
  align-items: center;
}
</style>
