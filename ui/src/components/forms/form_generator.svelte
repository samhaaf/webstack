
<script>
  import FormElement from './form_element.svelte';
  import {random_string} from '../utils/random.js';

  export let state = {};
  export let id = null;
  export let values;
  export let config;
  export let raw;

  let _this;
  let last_config;

  // if we're exporting raw
  if (raw !== -1){
    id = id || random_string(5);
  }
  $: if (_this) {
    raw = (document.getElementById(id) || {}).outerHTML;
  }

  // build component state
  state = Object.assign(
    { 'errors': [],    // component errors, not form errors
      'warnings': [],
      'children': [],
    },
    state || {}
  )
  function state_value (s) {
    // TODO better state from child states
    try {
      if (s.errors.length > 0) { return 'error' }
      if (s.warnings.length > 0) { return 'warning'}
      return 'ok'
    } catch (error) {
      return error
    }
  }

  // default values
  $: values = Object.assign(
    {'value': null},
    values || {}
  );
  // $: console.log('values', values);

  // assert that each of the keys in values is an expected key
  const expected_value_keys = ['status', 'errors', 'warnings', 'items', 'value'];
  for (var key in values) {
    if (!expected_value_keys.includes(key)) {
      state.errors = [...state.errors, {
        'message': `Incorrect key '${key}' found in 'values' attribute;`,
        'hint': `Correct structure of the 'values' attribute is: {
            'value': ...,
            'items': {...},
            'errors': [...],
            'warnings': [...],
            'status': 'ok' | 'error' | 'warning',
          }
        `
      }]
    }
  }

  // default config
  $: config = Object.assign({'errors': [], 'warnings': [], 'type': 'form'}, config || {});

  // assert config.type is not null
  if ( config.type == null ) {
    state.errors = [...state.errors, {
      'message': `'config' object has null value at key: 'type'`,
    }]
  }

  // if the config has items
  $: if ( Array.isArray(config.items) ) {

    // set default 'items' param in values object
    if (values.items == null) { values.items = {} };

    // iterate over the items
    for (const ix in config.items) {
      let item = config.items[ix];

      // assert that there is a 'name' in the item
      if (item.name != null) {

        // set default value for item
        values['items'] = Object.assign(
          {[item.name]: { value: (values.items[item.name] || {}).value || item.default || null } },
          values['items']
        )
        values['items'][item.name] = {
          value: (values.items[item.name] || {}).value || item.default || null
        }


      }

      // point from item config to related state object
      item._state = null;
      state.children = [...state.children, item._state] // this needs to rebuild on config change

      // stupid solution: add idx to every item to track updates. See below for TODO
      item._ix = ix;

    }

  }


  // TODO detect updates to config and track which items are the same
  $: if (config != last_config) {

    // compare names to set the last ids


    // update last_config
    last_config = Object.assign(config);
    // TODO attach name:id info to this object for future reference

  }

  // $: console.log('fg values', JSON.stringify(values));

</script>


<!-- * do something better here, like warning icon / window (env specific) -->

<!-- {#if state == null} -->
  <!-- <p>no state value</p> -->
<!-- {#if state == null}

  <FormElement {config} {id}
    bind:value={values.value} bind:state={state} >
    {#if Array.isArray(config.items) }
      {#each config.items as item} <!-- (item._ix) -->
        <!-- {#if item.name != null}
          <svelte:self
            config={item}
            bind:values={values.items[item.name]}
            bind:state={item._state}
            id={item.id}
          />
        {:else}
          <svelte:self
            config={item}
            bind:state={item._state}
            id={item.id}
          />
        {/if}
      {/each}
    {/if}
  </FormElement> -->

{#if true | state_value(state) == 'ok' | state_value(state) == 'warning' }

  {#if state_value(state) == 'warning' } -->
    warnings present
    <!-- TODO <Alert dismissable>{warning.message}</Alert>  -->
  {/if}

  <FormElement {config} {id}
    bind:this={_this}
    bind:value={values.value} bind:state={state} >
    {#if Array.isArray(config.items) }
      {#each config.items as item} <!-- (item._ix) -->
        {#if item.name != null}
          <svelte:self
            config={item}
            bind:values={values.items[item.name]}
            bind:state={item._state}
            id={item.id}
            raw={-1}
          />
        {:else}
          <svelte:self
            config={item}
            bind:state={item._state}
            id={item.id}
            raw={-1}
          />
        {/if}
      {/each}
    {/if}
  </FormElement>

{:else if state_value(state) == 'error'}
  ERROR: Failed to generate form. Errors:
  <!--  TODO <ScrollingDiv>{#each...}<Alert critical>{error.message}</Alert>... -->
  <ul>
    {#each state.errors as error}
      <li>
        <p>message: {error.message}</p>
        <p>hint: {error.hint}</p>
      </li>
    {/each}
  </ul>

{:else if state_value(state) != 'warning'}
  Unknown state value: <p>{state_value(state)}</p>
{/if}
