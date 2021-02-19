

<script>
  import Navbar from "./navbar.svelte";
  import HomeRoute from "./home/home_route.svelte";
  import FormsRoute from "./forms/forms_route.svelte";
	import GalleryRoute from "./gallery/gallery_route.svelte";
  import AboutRoute from "./about/about_route.svelte";
  import { Router, Route } from "svelte-routing";
  // import cssVars from './utils/svelte-css-vars';
  import cssVars from 'svelte-css-vars';

  export let url = "";

  let config = document.config.then((data) => { config = data });
  let css_vars = {};

  // $: console.log('config:', config)
  $: if (config.then == null) {
    for (var key in config.pallete) { css_vars["pallete-" + key] = config.pallete[key] }
  }
</script>


<main use:cssVars={css_vars}>
  {#await config}
    loading config..
  {:then config}
    <div class="content">
      <Router url="{url}">
        <Navbar/>
        <div class="route-content">
          <Route path="/"><HomeRoute/></Route>
          <Route path="/forms"><FormsRoute/></Route>
          <Route path="/gallery" component="{GalleryRoute}" />
          <Route path="/about" component="{AboutRoute}" />
        </div>
      </Router>
    </div>
  {:catch error}
    ERROR loading config
  {/await}
</main>


<style>
  main {

  }
  .content {
    background-color: var(--pallete-0);
    /* min-height: 100vh; */
    /* display: flex; */
    /* flex-direction: column; */
    /* max-height: 100vh; */
    /* overflow: hidden; */
  }
  /* .route-content {
    flex-grow: 1;
  } */
</style>
