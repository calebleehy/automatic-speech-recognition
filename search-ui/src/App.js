import React, { useEffect, useState } from "react";
import { SearchDriver } from "@elastic/search-ui";
import ElasticSearchConnector from "@elastic/search-ui-elasticsearch-connector";

const connector = new ElasticSearchConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions"
});

const driver = new SearchDriver({
  apiConnector: connector,
  searchQuery: {
    search_fields: {
      generated_text: {},
      age: {},
      gender: {},
      duration: {},
      accent: {}
    },
    result_fields: {
      generated_text: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      duration: { raw: {} },
      accent: { raw: {} }
    },
    facets: {
      gender: { type: "value" },
      accent: { type: "value" },
      age: { type: "value" }
    }
  }
});

function App() {
  const [state, setState] = useState(driver.getState());

  useEffect(() => {
    driver.subscribe(() => {
      setState(driver.getState());
    });
    driver.setSearchTerm("");
    driver.search();

    return () => driver.unsubscribe();
  }, []);

  // Render UI manually (SearchBox, Facets, Results, Paging, etc.)
  // because these components no longer exist in the package.

  return (
    <div>
      <input
        type="search"
        value={state.searchTerm}
        onChange={e => driver.setSearchTerm(e.target.value)}
        placeholder="Search generated_text, age, gender..."
      />
      <div>
        <h3>Facets</h3>
        {Object.entries(state.facets).map(([field, facet]) => (
          <div key={field}>
            <h4>{field}</h4>
            <ul>
              {facet.map(value => (
                <li key={value.value}>
                  <label>
                    <input
                      type="checkbox"
                      checked={value.selected}
                      onChange={() => driver.toggleSelectFacetValue(field, value.value)}
                    />
                    {value.value} ({value.count})
                  </label>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      <div>
        <h3>Results</h3>
        <ul>
          {state.results.map(result => (
            <li key={result.id}>
              <strong>{result.raw.generated_text}</strong><br />
              Age: {result.raw.age}, Gender: {result.raw.gender}, Accent: {result.raw.accent}, Duration: {result.raw.duration}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <button disabled={state.page === 1} onClick={() => driver.setCurrentPage(state.page - 1)}>Previous</button>
        <span> Page {state.page} </span>
        <button onClick={() => driver.setCurrentPage(state.page + 1)}>Next</button>
      </div>
    </div>
  );
}

export default App;
