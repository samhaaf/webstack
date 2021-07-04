
<div class='scroller mx-auto'>

  {#each tiles as tile}
    <div class={'card my-5 border-' + tile.status}>
      <div class='card-header bg-info text-light'>
        {tile.title}
      </div>
      {#if tile.status === 'success'}
        <div class='card-title bg-success text-light'>
          Success
        </div>
      {:else if tile.status === 'warning'}
        <div class='card-title bg-warning text-light'>
          Warning
        </div>
      {:else}
        <div class='card-title bg-danger text-light'>
          Failure
        </div>
      {/if}
      {#if tile.content}
        <div class='card-body'>
          <pre>{tile.content}</pre>
        </div>
      {/if}
    </div>
  {/each}

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
    max-height: 300px;
  }
</style>


<script>

  /* Utility Functions */
	async function fetch_resource(endpoint) {
    const response = await fetch(config.api_url + '/' + endpoint)//, {'mode': 'no-cors'})
    if (response.ok) {
      return response.json()
    } else {
      throw Error(JSON.stringify(response))
    }
  }

  function is_promise(item) {
    return !!item && typeof config.then === 'function'
  }


  /* Tests */

  let tiles = [];

  // Page load
  tiles = [...tiles, {
    title: '1. Page load',
    status: 'success',
  }]

  // Config load
  tiles = [...tiles, {title: '2. Remote config load'}]
  let config = document.config.then((data) => { config = data });
  $: config_loaded = !is_promise(config)
  $: tiles[1].status = config_loaded ? 'success' : 'danger'
  $: tiles[1].content = config_loaded ? JSON.stringify(config, null, 2) : ''

  // API test connect
  tiles = [...tiles, {
    title: '3. Connect to config.api_url + "/test"',
    status: 'warning',
    contnet: 'Depends on test 2'
  }]
  let test_result;
  $: if (!is_promise(config)) {
     test_result = fetch_resource('test').then( (test_result) => {
       tiles[2].status = 'success';
       tiles[2].content = JSON.stringify(test_result, null, 2);
     }).catch( (error) => {
       tiles[2].status = 'danger';
       tiles[2].content = JSON.stringify(error, null, 2);
     })
  }


  // API retrieve google sheet content
  tiles = [...tiles, {
    title: '4. Connect to API config.api_url + "/products"',
    status: 'warning',
    contnet: 'Depends on test 2'
  }]
  let products_result;
  $: if (!is_promise(config)) {
     products_result = fetch_resource('products').then( (products_result) => {
       tiles[3].status = 'success';
       tiles[3].content = JSON.stringify(products_result, null, 2);
     }).catch( (error) => {
       tiles[3].status = 'danger';
       tiles[3].content = JSON.stringify(error, null, 2);
     })
  }

</script>
