const handleChapterSelect = async (e) => {
    try {
      const selectedChaperId = e.value;
      setSections([]);
      setExercises([]);
      const ChaptersData = {
          Choices : selectedChaperId
      
        }
        const requestOptions = {
            method: 'GET', 
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(apiData)
          };
      const apiURL='http://localhost:4000/api/Filtered_Book/Chapter/'
      const response = await fetch(apiURL,requestOptions)
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      console.log(data)
      setSections(data.Sections);
      setExercises(data.Exercises);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };