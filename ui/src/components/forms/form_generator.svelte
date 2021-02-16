
<script>
  import FormElement from './form_element.svelte';

  export let state = {};
  export let id = null;
  export let values = {};
  export let config = {};

  let last_config;

  // build component state
  state = Object.assign(
    state || {},
    { 'errors': [],    // component errors, not form errors
      'warnings': [],
      'children': [],
      'value': function () {
        // if (this.children.length > 0) {
        //   if (this.children.someOf)
        // }
        if (this.errors.length > 0) { return 'error' }
        if (this.warnings.length > 0) { return 'warning'}
        return 'ok'
      },
    }
  )

  // assert that each of the keys in config is an expected key
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

  // assign defaults
  config = Object.assign({'errors': [], 'warnings': []}, config);
  values = Object.assign({'value': null}, values);


  // assert config.type is not null
  if ( config.type == null ) { state.errors.push({
      'message': `'config' object has null value at key: 'type'`,
  })}

  // if the config has items
  if ( Array.isArray(config.items) ) {

    // set default 'items' param in values object
    if (values.items == null) values.items = {};

    // iterate over the items
    for (const ix in config.items) {
      let item = config.items[ix];

      // console.log('item:', item);

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
      item._state = {};
      state.children = [...state.children, item._state] // this needs to rebuild on config change

      // stupid solution: add idx to every item to track updates. See below for TODO
      item._ix = ix;

    }

  }

  // console.log('name:_ix', config.name, config._ix);
  // console.log('config', config);
  // console.log('values', JSON.stringify(values));


  // TODO detect updates to config and track which items are the same
  $: if (config != last_config) {

    // compare names to set the last ids


    // update last_config
    last_config = Object.assign(config);
    // TODO attach name:id info to this object for future reference

  }

  $: console.log('state:', JSON.stringify(state));

</script>


<!-- * do something better here, like warning icon / window (env specific) -->

<!-- {#if state == null} -->
  <!-- <p>no state value</p> -->
{#if state == null || state.value() == 'ok' || state.value() == 'warning' }

  <!-- {#if state.value() == 'warning' } -->
    <!-- warnings present -->
    <!--  TODO <Alert dismissable>{warning.message}</Alert>  -->
  <!-- {/if} -->

  <FormElement {config} {id}
    bind:value={values.value} {state} >
    {#if Array.isArray(config.items) }
      {#each config.items as item} <!-- (item._ix) -->
        <svelte:self
          config={item}
          bind:values={values.items[item.name]}
          bind:state={item._state}
          id={item.id}
        />
      {/each}
    {/if}
  </FormElement>

{:else if state.value() == 'error'}
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
{:else if state.value() != 'warning'}
  Unknown state value: {state.value()}
{/if}
