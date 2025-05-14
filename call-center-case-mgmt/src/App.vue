<!-- App.vue -->
<template>
  <Layout>
    <template #sidebar>
      <SideBar />
    </template>

    <!-- Default slot (main content) -->
    <RouterView />
  </Layout>
</template>

<script>
import Layout from './components/Layout.vue'
import SideBar from './components/SideBar.vue'

export default {
  components: {
    Layout,
    SideBar
  }
}
</script>