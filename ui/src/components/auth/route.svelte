
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

</script>
