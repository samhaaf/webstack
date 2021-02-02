
<script>
  import Box from '../utils/box.svelte';
  import dayjs from 'dayjs';

  export let name;
  export let image_source;
  export let description;



</script>

<Box m-2 header={name}>
  <img src={"static/images/" + image_source} class="card-img-top"/>
  {description}
</Box>
