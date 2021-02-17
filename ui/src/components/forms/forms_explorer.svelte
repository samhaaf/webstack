
<script>
  import FormEditor from './form_editor.svelte';
  import FormGenerator from './form_generator.svelte';

  // // load config for given selection
  let form_group_key;
  let form_groups;
  let form_group;
  let major_versions;
  let major_version;
  let minor_versions;
  let minor_version;
  let config;
  let values = {};

  $: console.log('major_versions', major_versions);
  $: console.log('major_version', major_version);
  $: console.log('minor_versions', minor_versions);
  $: console.log('minor_version', minor_version);

  // wait until config loads and then load form_groups
  document.config.then((config) => {
    form_group_key = config.project_name + '.form_groups';

    // try to load & parse the form group
    try {
      form_groups = JSON.parse(localStorage.getItem(form_group_key));
    } catch (error) {
      // pass
    }

    if (form_groups != null) {
      console.log(`loaded form_groups from localStorage["${form_group_key}"]`);
    } else {
      console.log('using default form_groups');
      form_groups = [{
        'name': 'Test form 1',
        'versions': {
          0: {
            1: {
              'type': 'form',
              'items': [
                {
                  'type': 'string',
                  'name': 'first_name',
                  'label': 'First name:',
                  'placeholder': 'Ex. John',
                  'validations': [],  // default
                },{
                  'type': 'string',
                  'name': 'last_name',
                  'label': 'Last name:',
                  'placeholder': 'Ex. Smith',
                  'validations': [],  // default
                },{
                  'type': 'reset',
                },{
                  'type': 'submit',
                }
              ]
            }
          }
        }
      }]
    }
  })

  // persist changes to localStorage
  $: if (form_groups != null & form_group_key != null ) {
    if (localStorage.getItem(form_group_key) != JSON.stringify(form_groups) ) {
      localStorage.setItem(form_group_key, JSON.stringify(form_groups));
      console.log(`saved form_groups to localStorage["${form_group_key}"]`);
    }
  }

  // select major version
  $: if (form_group) {
    if ( form_group.versions == null ) { form_group.versions = {0: {0: {}}}}
    major_versions = Object.keys(form_group.versions);
    major_version = major_versions[major_versions.length-1];
  } else {
    major_versions = null;
    major_version = null;
  }

  // select minor version
  $: if (major_version) {
    minor_versions = Object.keys(form_group.versions[major_version]);
    minor_version = minor_versions[minor_versions.length-1];
    console.log('updating config');
    values = {};
    config = form_group.versions[major_version][minor_version]
  } else {
    minor_versions = null;
    minor_version = null;
    values = {};
    config = null;
  }

  // radio to switch select panels
  // TODO type: radio-panels
  let radio_value = 'existing';

  // Config object for creating a new form
  let new_form_values;
  let new_form_config = {
    type: 'form',
    items: [{
      type: 'string',
      label: 'Form name:',
      name: 'form_name'
    },{
      type: 'submit',
      text: 'Create',
      action: () => {
        form_groups = [
          ...form_groups,
          {'name': new_form_values.items.form_name.value}
        ];
        new_form_values = null;
        radio_value = 'existing';

      }
    }]
  }

  $: console.log('ex config', config);
  $: console.log('ex values', values);
</script>


<div class="form-selector">
  <h3>Form Selector</h3>
  <br>

  <input type='radio' id='existing' bind:group={radio_value} value='existing' />
  <label for='existing'>Select Existing</label>

  <input type='radio' id='new' bind:group={radio_value} value='new' />
  <label for='new'>Create New</label>

  {#if radio_value == 'existing'}

    <div class="form-groups-container">
      <label for='group-selector'>Form name:</label>
      <select bind:value={form_group} name='group-selector'>
        {#if form_groups != null}
          <option value={null}>---</option>
          {#each form_groups as group}
            <option value={group}>{group.name}</option>
          {/each}
        {/if}
      </select>
    </div>

    <div class="major-version-container">
      <label for='major-version-selector'>Major version:</label>
      <select bind:value={major_version} name='major-version-selector'>
        {#if major_versions != null}
          {#each major_version as version}
            <option value={version}>{version}</option>
          {/each}
        {/if}
      </select>
    </div>

    <div class="minor-version-container">
      <label for='minor-version-selector'>Minor version:</label>
      <select bind:value={minor_version} name='minor-version-selector'>
        {#if minor_versions != null}
          {#each minor_version as version}
            <option value={version}>{version}</option>
          {/each}
        {/if}
      </select>
    </div>

  {:else}

    <FormGenerator config={new_form_config} bind:values={new_form_values}/>

  {/if}

</div>

{#if config != null}
  <FormEditor bind:config={config} bind:values={values}/>
{/if}


<style>
  .form-selector {
    border: 2px outset;
    margin: 12px;
    padding: 6px;
    max-width: 650px;
    margin-left: auto;
    margin-right: auto;
  }
  select {
    min-width: 200px;
  }
</style>
