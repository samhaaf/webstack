<!--
{#await login_check}
{:then logged_in} -->
{#if ((logged_in === true) && !reversed) || ((logged_in === false) && reversed ) }
  <Route path={path}><slot/></Route>
{:else if ((logged_in === false) && !reversed) || ((logged_in === true) && reversed )}
  {#if return_to != null}
    <Route path={path}><Redirect href={redirect} {return_to}/></Route>
  {:else if return_here}
    <Route path={path}><Redirect href={redirect} return-here/></Route>
  {:else}
    <Route path={path}><Redirect href={redirect}/></Route>
  {/if}
{/if}


<script>

  import {Route} from 'svelte-routing';
  import Redirect from './redirect.svelte'

  export let path;
  export let logged_in;
  export let redirect = '/login'

  let reversed = ('reversed' in $$props) && ($$props['reversed'] != false)
  let return_here = ($$props['return-here'] == false) ? false : true
  let return_to = $$props['return-to'];
  
  console.log('return_here', return_here);

  console.log('reversed', reversed, (logged_in === true) || ((logged_in === false) && reversed ));

  // console.log('here6', login_check);
  //
  // login_check.then((logged_in) => {
  //   console.log('here7', logged_in);
  // })

</script>
