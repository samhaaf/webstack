
<div class='scroller mx-auto'>

  <div class='card my-5 border-success'>
    <div class='card-header bg-info text-light'>Page load</div>
    <div class='card-title bg-success text-light'>
      Success
    </div>
  </div>


  <div class={'card my-5 border-' + (config_loaded ? 'success' : 'danger')}>
    <div class='card-header bg-info text-light'>
      Remote config load
    </div>
    {#if config_loaded}
      <div class='card-title bg-success text-light'>
        Success
      </div>
      <div class='card-body'>
        Config load success:
        <pre class='bg-secondary text-light'>
          {JSON.stringify(config, null, 2)}
        </pre>
      </div>
    {:else}
      <div class='card-title bg-danger text-light'>
        Failure
      </div>
      <div class='card-body'>
        Config failed to load: {config}
      </div>
    {/if}
  </div>

</div>


<style>
  .scroller {
    max-width: 700px;
  }
  .card-header {
    font-size: 20px;
  }
  .card-title {
    background-color: lightgray;
    padding: 8px;
  }
  .card-body {
    font-size: 14px;
  }
  pre {
    background-color: lightgray;
  }
</style>


<script>
  let config = document.config.then((data) => { config = data });
  $: config_loaded = config && typeof config.then !== 'function'

</script>
