
<main use:cssVars={css_vars}>
  {#await config}
    loading config..
  {:then config}
    <div class="content pallete-0-5">
      <Router url="{url}">
        <Navbar/>
        <div class="route-content">
          <Route path="/"><HomeRoute/></Route>
          <Route path="/forms/manager/"><FormManager/></Route>
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
  .pallete-0 {
    background-color: var(--pallete-0);
  }
  .pallete-0-5 {
    background-color: var(--pallete-0-5);
  }
  .pallete-1 {
    background-color: var(--pallete-1);
  }
  .pallete-2 {
    background-color: var(--pallete-2);
  }
  .pallete-3 {
    background-color: var(--pallete-3);
  }
  .pallete-4 {
    background-color: var(--pallete-4);
  }

</style>


<script>
  import Navbar from "./navbar.svelte";
  import HomeRoute from "./home/home_route.svelte";
  import FormsRoute from "./forms/forms_route.svelte";
  import FormManager from "./forms/form_manager.svelte";
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
