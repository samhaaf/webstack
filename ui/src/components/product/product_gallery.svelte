
<script>
  import ProductView from './product_view.svelte';
  import Box from '../utils/box.svelte';
  import dayjs from 'dayjs';

  // let products = [
  //   {
  //     name: 'Apple',
  //     image: 'static/images/apple.png'
  //   },
  //   {
  //     name: 'Banana',
  //     image: 'static/images/banana.jpg'
  //   },
  //   {
  //     name: 'Orange',
  //     image: 'static/images/orange.jpg'
  //   },
  //   {
  //     name: 'Coconut',
  //     image: 'static/images/coconut.jpg'
  //   },
  //   {
  //     name: 'Pineapple',
  //     image: 'static/images/pineapple.jpg'
  //   }
  // ];


	async function fetch_products() {
		const response = await fetch('http://localhost:8000/products');

		if (response.ok) {
			return response.json();
		} else {
			throw new Error(response);
		}
	}

  let promise = fetch_products();

</script>

<!-- <div class="m-1 p-2 row product-gallery"> -->
<div class="product-gallery d-flex flex-wrap justify-content-center">

  {#await promise}
    <p>waiting...</p>
  {:then products}
  	{#each products as {name, image_source, description}, idx (name)}
      {#if [name, image_source, description].some((x)=>x)}
        <div class="product">
      		<ProductView {name} {image_source} {description}/>
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
