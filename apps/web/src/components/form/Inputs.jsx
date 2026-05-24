import { FormField } from "./FormField";

export function TextInput({ label, hint, value, onChange, placeholder = "" }) {
  return (
    <FormField label={label} hint={hint}>
      <input className="form-input" type="text" value={value} placeholder={placeholder} onChange={onChange} />
    </FormField>
  );
}

export function NumberInput({ label, hint, value, onChange, placeholder = "", min, step = "any" }) {
  return (
    <FormField label={label} hint={hint}>
      <input
        className="form-input"
        type="number"
        min={min}
        step={step}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
      />
    </FormField>
  );
}

export function SelectInput({ label, hint, value, onChange, options }) {
  return (
    <FormField label={label} hint={hint}>
      <select className="form-input" value={value} onChange={onChange}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </FormField>
  );
}

export function TextAreaInput({ label, hint, value, onChange, rows = 4, placeholder = "" }) {
  return (
    <FormField label={label} hint={hint}>
      <textarea
        className="form-input form-textarea"
        rows={rows}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
      />
    </FormField>
  );
}

