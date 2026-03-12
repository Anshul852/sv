<script lang="ts">
  import SilentStudyRooms from '$lib/components/rooms/SilentStudyRooms.svelte';
  import { onMount } from 'svelte';

  let mounted = false;
  onMount(() => mounted = true);
</script>

<div class="rooms-page" class:mounted>
    <SilentStudyRooms />
</div>

<style>
  .rooms-page {
    padding: 28px 32px 48px;
    max-width: 1200px;
    margin: 0 auto;
    height: calc(100vh - 80px);
    opacity: 0;
    transition: opacity 0.5s ease;
  }
  .rooms-page.mounted { opacity: 1; }
</style>
