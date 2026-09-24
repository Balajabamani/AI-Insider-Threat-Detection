import { useEffect, useState } from "react";

function EmployeeStatus() {

  const [employees, setEmployees] = useState([]);

  // ============================================================
  // LOAD EMPLOYEE STATUS
  // ============================================================

  const loadEmployees = () => {

    fetch("http://127.0.0.1:8000/risk-ranking")

      .then((res) => {

        if (!res.ok) {
          throw new Error(
            "Failed to load employee status"
          );
        }

        return res.json();

      })

      .then((data) => {

        setEmployees(data);

      })

      .catch((error) => {

        console.error(
          "Error loading employee status:",
          error
        );

      });

  };


  // ============================================================
  // REAL-TIME POLLING
  // ============================================================

  useEffect(() => {

    // Load immediately
    loadEmployees();


    // Refresh every 2 seconds
    const interval = setInterval(
      loadEmployees,
      2000
    );


    return () => {

      clearInterval(interval);

    };

  }, []);


  // ============================================================
  // STATUS COLOR
  // ============================================================

  const getStatusColor = (status) => {

    switch (String(status).toUpperCase()) {

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


  // ============================================================
  // UI
  // ============================================================

  return (

    <div className="status-section-inner">

      <h2>
        🏢 Employee Status Monitor
      </h2>


      <div className="employee-status-grid">

        {employees.length > 0 ? (

          employees.map(
            (employee, index) => (

              <div
                className="employee-status-card"
                key={`${employee.name}-${index}`}
              >

                <div
                  className="status-dot"
                  style={{
                    backgroundColor:
                      getStatusColor(
                        employee.status
                      )
                  }}
                ></div>


                <h3>
                  {employee.name}
                </h3>


                <p>
                  {employee.department}
                </p>


                <strong
                  style={{
                    color:
                      getStatusColor(
                        employee.status
                      )
                  }}
                >
                  {employee.status}
                </strong>


                <span
                  style={{
                    marginTop: "8px",
                    fontSize: "16px",
                    color: "#607d8b"
                  }}
                >
                  Risk: {employee.risk}%
                </span>

              </div>

            )

          )

        ) : (

          <p>
            No employee status data available.
          </p>

        )}

      </div>

    </div>

  );

}


export default EmployeeStatus;