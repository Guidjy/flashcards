export default function Table({ columns, rows }) {
  return (
    <>
      <div className="overflow-x-auto rounded-box border border-base-content/5 bg-base-100">
        <table className="table">
          {/* head */}
          <thead>
            <tr>
              <th></th>
              {columns.map((column, index) => {
                return (
                  <th key={index}>{column}</th>
                );
              })}
            </tr>
          </thead>
          <tbody>
          {/* rows */}
          {rows.map((row) => {
            return (
              row
            );
          })}
          </tbody>
        </table>
      </div>
    </>
  )
}