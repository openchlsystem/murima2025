
<template>
  <div class="home">
    <div class="container py-5">
      <div class="row">
        <div class="col-md-8 mx-auto text-center">
          <h1 class="display-4 mb-4">Welcome Home</h1>
          <p class="lead mb-5">A simple and clean homepage built with Bootstrap</p>
        </div>
      </div>

      <div class="row">
        <div class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Feature One</h5>
              <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
              <button class="btn btn-primary">Learn More</button>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Feature Two</h5>
              <p class="card-text">Sed do eiusmod tempor incididunt ut labore et dolore magna.</p>
              <button class="btn btn-primary">Learn More</button>
            </div>
          </div>
        </div>

        <div class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Feature Three</h5>
              <p class="card-text">Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
              <button class="btn btn-primary">Learn More</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
