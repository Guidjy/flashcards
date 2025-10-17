export function Form({ title, fields, onSubmit, buttonText }) {
  return (
    <form className="w-full md:w-xl lg:w-lg mx-10" onSubmit={ (event) => {event.preventDefault(); onSubmit();} }>
      <fieldset className="fieldset bg-base-200 border-base-300 rounded-box border p-4">
        <legend className="fieldset-legend">{title}</legend>
        {fields.map((field, index) => (
          <FormField
            key={index}
            label={field.label}
            type={field.type}
            placeholder={field.placeholder}
            onChange={field.onChange}
          />
        ))}
        <button type="submit" className="btn btn-primary my-2">{buttonText}</button>
      </fieldset>
    </form>
  );
}


export function FormField({label, type, placeholder, onChange}) {
  return (
    <>
      <label className="label">{label}</label>
      {type === "file" ? (
        <input type={type} onChange={onChange} className="file-input file-input-primary mb-2 w-full" placeholder={placeholder} />
      ) : (
        <input type={type} onChange={onChange} className="input mb-2 w-full" placeholder={placeholder} />
      )}
    </>
  );
}