

<script>
  import { Router, Link, Route } from "svelte-routing";
	import HomeRoute from "./home/home_route.svelte";
	import ProductRoute from "./product/product_route.svelte";
  import AboutRoute from "./about/about_route.svelte";

  export let url = "";

  // await document.__env_promise__;
  console.log(2);
  console.log(document.__env_promise__);
  console.log(document.__env__);

  $: env = document.__env__;
  if (env) {
    console.log(env);
    console.log(env.api_url);
  }


</script>


<main>

	<Router url="{url}">
		<nav>
			<Link to="/">Home</Link>
			<Link to="/products">Products</Link>
			<Link to="/about">About</Link>
		</nav>
		<div>
			<Route path="/"><HomeRoute/></Route>
			<Route path="/products" component="{ProductRoute}" />
			<!-- <Route path="product/:id" component="{BlogPost}" /> -->
			<!-- <Route path="product/:id"><BlogPost {id}/></Route> -->
			<!-- <Route path="product/:id" let:params><BlogPost id="{params.id}""/></Route> -->
			<Route path="about" component="{AboutRoute}" />
		</div>
    <div>
      <p>{env}</p>
    </div>
	</Router>


</main>
