async function fetchPreviousScores() {
    const teamId = 117; // Houston Astros ID
    // Calculate dates for the last 10 days to ensure we get finished games
    const today = new Date();
    const tenDaysAgo = new Date(today);
    tenDaysAgo.setDate(today.getDate() - 10);
    
    const startDate = tenDaysAgo.toISOString().split('T')[0];
    const endDate = today.toISOString().split('T')[0];

    const url = `https://statsapi.mlb.com/api/v1/schedule?teamId=${teamId}&startDate=${startDate}&endDate=${endDate}&sportId=1`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        // Filter for games that are actually finished (Final)
        const games = data.dates
            .flatMap(date => date.games)
            .filter(game => game.status.abstractGameState === "Final")
            .reverse() // Most recent first
            .slice(0, 5); // Just take the last 5

        const container = document.getElementById('scores-container');
        container.innerHTML = ''; // Clear loading text

        games.forEach(game => {
            const awayTeam = game.teams.away.team.name;
            const homeTeam = game.teams.home.team.name;
            const awayScore = game.teams.away.score;
            const homeScore = game.teams.home.score;
            const gameDate = new Date(game.gameDate).toLocaleDateString();

            const gameRow = document.createElement('div');
            gameRow.className = 'score-row';
            gameRow.innerHTML = `
                <span>${gameDate}</span>: 
                <strong>${awayTeam} ${awayScore}</strong> vs <strong>${homeTeam} ${homeScore}</strong>
            `;
            container.appendChild(gameRow);
        });
    } catch (error) {
        console.error("Error fetching scores:", error);
        document.getElementById('scores-container').innerHTML = "<p>Unable to load previous scores.</p>";
    }
}

// Call this function when the window loads
window.onload = () => {
    // Keep your existing fetchGame logic here
    fetchPreviousScores();
};
