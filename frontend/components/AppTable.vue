<template>
  <table class="border-collapse border border-red-500">
    <thead>
      <tr>
        <th>RANK</th>
        <th>NAME</th>
        <th>AGE</th>
        <th>POINTS</th>
        <th>COUNTRY</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(ranking, index) in rankings" :key="index">
        <td>{{ ranking.rank }}</td>
        <td>{{ ranking.name }}</td>
        <td>{{ ranking.age }}</td>
        <td>{{ ranking.points }}</td>
        <td>{{ ranking.country}}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>
  const { data: rankings } = await useFetch('http://127.0.0.1:5000/get_data')
</script>