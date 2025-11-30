<script>
  export let label = 'Button';
  export let primary = true;
</script>

<button
  class:primary
  on:click
>
  {label}
</button>

<style>
  button {
    padding: 10px 20px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
  }
  
  button:hover {
    transform: translateY(-1px);
  }

  .primary {
    background: #4f46e5;
    color: white;
  }
</style>
