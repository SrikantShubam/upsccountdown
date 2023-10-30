document.querySelector("#submitQuestion").addEventListener("click", function(e) {
    e.preventDefault();  // Prevent form submission
    
    let userQuery = document.querySelector("#userInput").value;
    let baseURL = "https://www.perplexity.ai/search?";
    let encodedQuery = encodeURIComponent(userQuery);
    let fullURL = baseURL + "q=" + encodedQuery + "&copilot=false";
    window.open(fullURL, '_blank');
 
});