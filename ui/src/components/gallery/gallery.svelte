
<script>
  import Item from './item.svelte';
  import Box from '../utils/box.svelte';
  import dayjs from 'dayjs';

	async function fetch_items() {
    await document.config;
		const response = await fetch(document.config.api_url + '/products');

		if (response.ok) {
			return response.json();
		} else {
			throw new Error(response);
		}
	}

  let promise = fetch_items();
</script>


<div class="gallery d-flex flex-wrap justify-content-center">

  {#await promise}
    <p>waiting...</p>
  {:then items}
  	{#each items as {name, image_source, description}, idx (name)}
      {#if [name, image_source, description].some((x)=>x)}
        <div class="item">
      		<Item {name} {image_source} {description}/>
        </div>
      {/if}
  	{/each}
  {:catch error}
    <p>ERROR: {error.message}</p>
  {/await}

</div>


<style>
  .product {
    width: 300pt;
    min-height: 300pt;
  }

  .product-gallery {
    min-height: 100%;
  }
</style>
