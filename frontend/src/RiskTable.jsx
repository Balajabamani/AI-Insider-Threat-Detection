import { useEffect, useState } from "react";


function RiskTable() {

  const [employees, setEmployees] = useState([]);


  const loadRiskRanking = () => {

    fetch("http://127.0.0.1:8000/risk-ranking")

      .then((response) => {

        if (!response.ok) {

          throw new Error(
            "Risk ranking request failed"
          );

        }

        return response.json();

      })

      .then((data) => {

        setEmployees(
          Array.isArray(data)
            ? data
            : []
        );

      })

      .catch((error) => {

        console.error(
          "Risk ranking error:",
          error
        );

      });

  };


  useEffect(() => {

    // Initial load
    loadRiskRanking();


    // Update every 2 seconds
    const interval = setInterval(
      loadRiskRanking,
      2000
    );


    return () => {

      clearInterval(interval);

    };

  }, []);


  const getStatusColor = (status) => {

    switch (status) {

      case "HIGH":
        return "#ef4444";

      case "MEDIUM":
        return "#f59e0b";

      case "LOW":
        return "#2563eb";

      case "SAFE":
        return "#16a34a";

      default:
        return "#16a34a";

    }

  };


  return (

    <div className="risk-table">

      <h2>
        👥 Employee Risk Ranking
      </h2>


      <table>

        <thead>

          <tr>

            <th>
              Employee
            </th>

            <th>
              Department
            </th>

            <th>
              Risk Score
            </th>

            <th>
              Status
            </th>

          </tr>

        </thead>


        <tbody>

          {employees.length > 0 ? (

            employees.map(
              (employee, index) => (

                <tr
                  key={
                    `${employee.name}-${index}`
                  }
                >

                  <td>
                    {employee.name}
                  </td>

                  <td>
                    {employee.department}
                  </td>

                  <td>
                    {employee.risk}%
                  </td>

                  <td
                    style={{
                      fontWeight: "bold",
                      color:
                        getStatusColor(
                          employee.status
                        )
                    }}
                  >

                    {employee.status}

                  </td>

                </tr>

              )

            )

          ) : (

            <tr>

              <td
                colSpan="4"
                style={{
                  textAlign: "center",
                  padding: "30px"
                }}
              >

                No employee risk data available.

              </td>

            </tr>

          )}

        </tbody>

      </table>

    </div>

  );

}


export default RiskTable;