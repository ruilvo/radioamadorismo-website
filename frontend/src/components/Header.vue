<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/"
        >Portal do radioamadorismo</router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" exact-active-class="active" to="/"
              >Início</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              exact-active-class="active"
              to="/repetidores"
              >Repetidores</router-link
            >
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              API
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li>
                <a class="dropdown-item" href="/api/v1/repeaters"
                  >Repetidores</a
                >
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div class="container-fluid">
    <p>Um projeto de Rui "CT7ALW" Oliveira</p>
  </div>
</template>

<script>
export default {
  name: "Header",
};
</script>
