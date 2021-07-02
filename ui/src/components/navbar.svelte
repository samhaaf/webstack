

<nav>
  <Link to="/" getProps={getProps('/')} >
    <img src="/logo.png" class="logo left" alt="3649.design"/>
  </Link>
  <div class='nav-button-container'>
    <Link getProps={getProps('/spaces')} to="/spaces">
      <div class="nav-button">Spaces</div>
    </Link>
    <Link getProps={getProps('/styles')} to="/styles">
      <div class="nav-button">Styles</div>
    </Link>
    <Link getProps={getProps('/forms')} to="/forms">
      <div class="nav-button">Forms</div>
    </Link>
    <Link getProps={getProps('/gallery')} to="/gallery">
      <div class="nav-button">Gallery</div>
    </Link>
    <Link getProps={getProps('about')} to="/about">
      <div class="nav-button">About</div>
    </Link>
  </div>
</nav>


<style>
  nav {
    min-width: 100%;
    /* border: 1px solid; */
    background-color: var(--pallete-2);
    display: flex;
    flex-direction: row;
  }

  .nav-button-container {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-end;
    align-items: center;
    margin-left: auto;
  }

  .nav-button-container :global(a) {
    height: calc(100% - 12px);
    border-style: outset;
    border-width: 0;
  }

  .nav-button-container :global(a.active) {
    height: calc(100% - 12px);
    border-style: inset;
    border-width: 0;
  }

  .nav-button {
    display: flex;
    align-items: center;
    border-width: 2px ;
    border-color: var(--pallete-3);
    border-style: inherit;
    padding: 0 12px 0 12px;
    margin: 0 6px 0 0;
    height: 100%;
    background-color: var(--pallete-3);
  }

  .nav-button {
    color: var(--pallete-0);
  }

  .logo {
    max-width: 55px;
    margin: 3px;
    background-color: var(--pallete-0-5);
  }
</style>


<script>
  import { Router, Link } from "svelte-routing";
  // import cssVars from './utils/svelte-css-vars';
  import cssVars from 'svelte-css-vars';

  let config = document.config;


  function getProps(to) {

    function inner_fn({ location, href, isPartiallyCurrent, isCurrent }) {
      let props = {
        class: "link-a"
      }

      const isActive = href === to ? isCurrent : isPartiallyCurrent || isCurrent;
      if (isActive) {
        props.class += ' active'
      } else {
        props.class += ' inactive'
      }
      return props;
    }

    return inner_fn
  }

</script>
