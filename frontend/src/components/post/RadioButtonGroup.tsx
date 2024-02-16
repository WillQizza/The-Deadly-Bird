import styles from './RadioButtonGroup.module.css'
import { ToggleButtonGroup, ToggleButton } from 'react-bootstrap';

interface RadioOptionProps {
    value: string,
    label: string
}

interface RadioButtonGroupProps {
    name: string,
    defaultValue: string,
    options: RadioOptionProps[],
    valueRef: { current: string }
}

const RadioButtonGroup: React.FC<RadioButtonGroupProps> = (props: RadioButtonGroupProps) => {
    const { name, defaultValue, options, valueRef } = props;

    return (
        <>
            <ToggleButtonGroup
                name={name}
                type='radio'
                defaultValue={defaultValue}
            >
                {options.map((option, index) => (
                    <ToggleButton
                        key={index}
                        id={`${name}-radio-${index}`}
                        value={option.value}
                        onChange={(e) => valueRef.current = option.value}
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