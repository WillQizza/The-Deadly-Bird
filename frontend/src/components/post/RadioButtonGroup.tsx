import styles from './RadioButtonGroup.module.css'
import { ToggleButtonGroup, ToggleButton } from 'react-bootstrap';

interface RadioOptionProps {
    value: string,
    label: string
}

interface RadioButtonGroupProps {
    name: string,
    options: RadioOptionProps[],
    value: string,
    setValue: React.Dispatch<React.SetStateAction<string>>
}

const RadioButtonGroup: React.FC<RadioButtonGroupProps> = (props: RadioButtonGroupProps) => {
    const { name, options, value, setValue } = props;

    return (
        <>
            <ToggleButtonGroup
                name={name}
                type='radio'
                value={value}
            >
                {options.map((option, index) => (
                    <ToggleButton
                        key={index}
                        id={`${name}-radio-${index}`}
                        value={option.value}
                        onChange={(e) => {
                            setValue(option.value);
                        }}
                        variant='outline-secondary'
                        className={styles.radioSelectOption}
                    >
                        {option.label}
                    </ToggleButton>
                ))}
            </ToggleButtonGroup>
        </>
    );
}

export default RadioButtonGroup;