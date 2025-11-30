<script lang="ts">
  import { Canvas } from '@threlte/core';
  import { useGltf, OrbitControls, Environment } from '@threlte/extras';

  export let modelUrl: string;
  export let autoRotate = true;

  const { gltf } = useGltf(modelUrl);
</script>

<div class="w-full h-full relative">
  <Canvas>
    <Environment preset="city" />
    <OrbitControls {autoRotate} enableZoom={true} />
    
    {#if $gltf}
      <primitive object={$gltf.scene} scale={2} />
    {/if}
  </Canvas>
</div>
